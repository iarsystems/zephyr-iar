#
# Copyright 2025 NXP
#
# SPDX-License-Identifier: Apache-2.0

if(CONFIG_SOC_MIMX8MN6_A53)
  board_runner_args(jlink "--device=MIMX8MN6_A53_0" "--no-reset" "--flash-sram")
  board_runner_args(iar "--device=MIMX8MN6_A53")

  include(${ZEPHYR_BASE}/boards/common/jlink.board.cmake)
  include(${ZEPHYR_BASE}/boards/common/iar.board.cmake)
endif()
