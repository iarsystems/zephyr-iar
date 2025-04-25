# Copyright (c) 2025 IAR Systems.
#
# SPDX-License-Identifier: Apache-2.0

"""Runner for flashing through CSpyBat, the official command-line
   interface to the C-SPY debugger from IAR Systems.
"""

import argparse
import os
from pathlib import Path

from runners.core import RunnerCaps, RunnerConfig, ZephyrBinaryRunner, BuildConfiguration

class CSpyBinaryRunner(ZephyrBinaryRunner):
   """Runner front-end for CSpyBat"""

   def __init__(
      self,
      cfg: RunnerConfig,
      port: str,
      device: str,
      board_file: Path | None,
      frequency: int,
      ewarm: Path | None,
      use_elf: bool,
      dmac_file: Path | None,
      ddf_file: Path | None,
      semihost: bool,
      cpu:      str,
   ) -> None:
      super().__init__(cfg)

      self._port         = port
      self._device       = device
      self._board_file   = board_file
      self._frequency    = frequency
      self._ewarm        = ewarm
      self._dmac_file    = dmac_file
      self._use_elf      = use_elf
      self._ddf_file     = ddf_file
      self._semihost     = semihost
      self._cpu          = cpu

   @classmethod
   def _get_iar_toolchain_path(self) -> Path:
      """Obtain the path to an IAR ARM toolchain path. For an EWARM installation,
      this would mean <path-to-EWARM>/arm
      """

      # Set the toolchain path to IAR_TOOLCHAIN_PATH environment variable if set,
      # otherwise if not set or the path is invalid, try to look for an
      # EWARM installation in PATH
      if os.getenv("IAR_TOOLCHAIN_PATH") is not None:
         if Path(os.getenv("IAR_TOOLCHAIN_PATH")).exists():
            iar_toolchain_path = Path(os.getenv("IAR_TOOLCHAIN_PATH"))
            return iar_toolchain_path
      # Search in PATH for an EWARM installation
      else:
         os_path = os.getenv("PATH").split(os.pathsep)
         for path in os_path:
            if path.find("EWARM") > -1:
               iar_toolchain_path = Path(os.path.join(path, "arm"))
               if iar_toolchain_path.exists():
                  return iar_toolchain_path

      raise NotImplementedError((
         "Could not find a valid IAR embedded workbench for ARM installation."
         " You can either supply a path through --ewarm=<path-to-EWARM-installation>, you can set the IAR_TOOLCHAIN_PATH environment variable"
         " (https://docs.zephyrproject.org/latest/develop/toolchains/iar_arm_toolchain.html), or add an EWARM installation to your PATH."
      ))

   @classmethod
   def _get_cspybat_path(self, iar_toolchain_path) -> str:
      iar_ew_dir = iar_toolchain_path.parent.absolute() # get main EW parent dir
      iar_ew_common_dir = Path(os.path.join(iar_ew_dir, 'common'))

      if iar_ew_common_dir.exists():
         cspybat_exe_path = os.path.join(iar_ew_common_dir, 'bin', 'CSpyBat.exe')
         if Path(cspybat_exe_path).exists():
            return cspybat_exe_path
         else:
            raise NotImplementedError(f"path to CSpyBat executable {cspybat_exe_path} does not exist.")

      raise NotImplementedError("could not determine path to CSpyBat.exe. Do you have a valid Embedded Workbench installation?")

   @classmethod
   def name(cls):
      return "cspy"

   @classmethod
   def capabilities(cls):
      return RunnerCaps(commands={'flash'}, rtt=True, erase=True)

   @classmethod
   def do_add_parser(cls, parser):
      ## Required arguments ##
      parser.add_argument(
         "--port",
         type=str,
         choices=["swd", "jtag", "cjtag"],
         default="swd",
         required=True,
         help="Interface identifier",
      )
      parser.add_argument(
         "--device",
         type=str,
         required=True,
         help="Device name",
      )
      parser.add_argument(
         "--board-file",
         type=Path,
         required=True,
         help="Target device .board file"
      )
      parser.add_argument(
         "--cpu",
         type=str,
         required=True,
         help="CPU name",
      )

      ## Optional arguments ##
      # TODO: make port & device optional if xcl files supplied?
      # parser.add_argument(
      #    "--xcl-general-file",
      #    type=Path,
      #    required=False,
      #    help="Path to xcl file describing the general portion of the CSpyBat args.",
      # )
      # parser.add_argument(
      #    "--xcl-driver-file",
      #    type=Path,
      #    required=False,
      #    help="Path to xcl file describing the driver portion of the CSpyBat args.",
      # )
      parser.add_argument(
         "--frequency",
         type=int,
         required=False,
         help="Programmer frequency in KHz",
      )
      parser.add_argument(
         "--ewarm",
         type=Path,
         required=False,
         help="Path to EWARM installation",
      )
      parser.add_argument(
         "--reset-mode",
         type=str,
         required=False,
         choices=["sw", "hw", "core"],
         help="Reset mode",
      )
      parser.add_argument(
         "--use-elf",
         action="store_true",
         required=False,
         help="Use ELF file when flashing instead of HEX file",
      )
      parser.add_argument(
         "--jet-power-from-probe",
         required=False,
         help="Set target power from i-jet to be left on or switched off after debugging",
      )
      parser.add_argument(
         "--dmac-file",
         required=False,
         help="Target device macro file (.dmac)"
      )
      parser.add_argument(
         "--ddf-file",
         required=False,
         help="Target device description file (.ddf)"
      )
      parser.add_argument(
         "--semihost",
         type=bool,
         default=False,
         required=False,
         help="Enable semihosting",
      )

   @classmethod
   def do_create(
      cls, cfg: RunnerConfig, args: argparse.Namespace
   ) -> "CSpyBinaryRunner":
      return CSpyBinaryRunner(
         cfg,
         port=args.port,
         device=args.device,
         board_file=args.board_file,
         frequency=args.frequency,
         ewarm=args.ewarm,
         dmac_file=args.dmac_file,
         ddf_file=args.ddf_file,
         use_elf=args.use_elf,
         semihost=args.semihost,
         cpu=args.cpu
      )

   def do_run(self, command: str, **kwargs):
      if command == "flash":
         try:
            self.flash(**kwargs)
         except Exception as e:
            print(f"Error during flashing process: {str(e)}")

   def flash(self, **kwargs) -> None:
      build_cfg = BuildConfiguration(self.cfg.build_dir)

      # Get the EWARM path if set
      if self._ewarm:
         ewarm_path = self._ewarm
      else:
         ewarm_path = None

      # Set the IAR ARM toolchain path
      if ewarm_path is None:
         iar_toolchain_path = self._get_iar_toolchain_path()
      else:
         if ewarm_path.exists():
            iar_toolchain_path = Path(os.path.join(ewarm_path, "arm"))
         else:
            raise NotImplementedError(f"provided path to EWARM installation {ewarm_path} does not exist.")

      toolchain_bin = os.path.join(iar_toolchain_path, "bin")

      ## Set the general portion of the cspybat args ##
      general_args = f"{os.path.join(toolchain_bin, "armproc.dll")} {os.path.join(toolchain_bin, "armjet.dll")}"

      if self._use_elf:
         # Use elf file if instructed to do so.
         dl_file = self.cfg.elf_file
      elif self.cfg.hex_file is not None:
         dl_file = self.cfg.hex_file
      else:
         dl_file = None

      if dl_file is None:
         raise RuntimeError('cannot flash: no download file was specified')
      elif not os.path.isfile(dl_file):
         raise RuntimeError(f'download file {dl_file} does not exist')
      else:
         general_args += f" {dl_file}"

      general_args += f" --plugin={os.path.join(toolchain_bin, "armLibSupportUniversal.dll")}"

      if self._dmac_file:
         general_args += f" --device_macro={self._dmac_file}"

      if self._board_file:
         if self._board_file.exists():
            general_args += f" --flash_loader={self._board_file}"
         else:
            raise RuntimeError(f".board file {self._board_file} does not exist")
      else:
         raise RuntimeError("No .board file specified.")

      # Omit sign-on message
      general_args += " --silent"

      # Exit after flash if not semihosting
      if not self._semihost:
         general_args += " --timeout=0 --leave_target_running"

      ## Set the driver portion of the cspybat args (applied after --backend) ##
      driver_args = " --backend --suppress_entrypoint_warning"

      if self._port:
         driver_args += f" --drv_interface={self._port.upper()}"
      else:
         raise RuntimeError("No port specified.")

      driver_args += " --jet_power_from_probe=leave_on"

      if self._device:
         driver_args += f" --device={self._device}"
      else:
         raise RuntimeError("No device specified.")

      if self._frequency:
         driver_args += f" --drv_interface_speed={self._frequency}"

      # Add board file
      if self._board_file:
         driver_args += f" --board_file={self._board_file}"

      if self._ddf_file:
         driver_args_old += f" -p {self._ddf_file}"

      if self._semihost:
         driver_args += " --semihosting"

      max_num_cpus = build_cfg.get("CONFIG_MP_MAX_NUM_CPUS")
      if max_num_cpus:
         driver_args += f" --multicore_nr_of_cores={max_num_cpus}"

      if build_cfg.get("CONFIG_LITTLE_ENDIAN"):
         driver_args += f" --endian=little"
         endian = "little"
      else:
         driver_args += f" --endian=big"
         endian = "big"

      if self._cpu:
         driver_args += f" --cpu={self._cpu}"
      else:
         RuntimeError("No CPU name specified")

      cspybat_exe_path = self._get_cspybat_path(iar_toolchain_path)

      cmd = cspybat_exe_path + " " + general_args + driver_args

      self.check_call(cmd)
