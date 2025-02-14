/*
 *
 * Copyright (c) 2025 IAR Systems AB
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_ARCH_RISCV_RISCV_PRIVILEGED_ASM_INLINE_IAR_H_
#define ZEPHYR_INCLUDE_ARCH_RISCV_RISCV_PRIVILEGED_ASM_INLINE_IAR_H_

#include <intrinsics.h>

#define _CSR_mcause           (0x342)
#define _CSR_mhartid          (0xF14)
#define _CSR_mip              (0x344)
#define _CSR_mie              (0x304)

#define _CSR_pmpcfg0          (0x3A0)
#define _CSR_pmpcfg1          (0x3A1)
#define _CSR_pmpcfg2          (0x3A2)
#define _CSR_pmpcfg3          (0x3A3)
#define _CSR_pmpcfg4          (0x3A4)
#define _CSR_pmpcfg5          (0x3A5)
#define _CSR_pmpcfg6          (0x3A6)
#define _CSR_pmpcfg7          (0x3A7)

#define _CSR_pmpaddr0          (0x3B0)
#define _CSR_pmpaddr1          (0x3B1)
#define _CSR_pmpaddr2          (0x3B2)
#define _CSR_pmpaddr3          (0x3B3)
#define _CSR_pmpaddr4          (0x3B4)
#define _CSR_pmpaddr5          (0x3B5)
#define _CSR_pmpaddr6          (0x3B6)
#define _CSR_pmpaddr7          (0x3B7)
#define _CSR_pmpaddr8          (0x3B8)
#define _CSR_pmpaddr9          (0x3B9)
#define _CSR_pmpaddr10          (0x3BA)
#define _CSR_pmpaddr11          (0x3BB)
#define _CSR_pmpaddr12          (0x3BC)
#define _CSR_pmpaddr13          (0x3BD)
#define _CSR_pmpaddr14          (0x3BE)
#define _CSR_pmpaddr15          (0x3BF)

#define csr_read(csr) __read_csr(_CSR_ ## csr)

#define csr_write(csr, val) __write_csr(_CSR_ ## csr, val)

#define csr_read_set(csr, val) __set_bits_csr(_CSR_ ## csr, val)
#define csr_set(csr, val)      __set_bits_csr(_CSR_ ## csr, val)

#define csr_read_clear(csr, val) __clear_bits_csr(_CSR_ ## csr, val)
#define csr_clear(csr, val)      __clear_bits_csr(_CSR_ ## csr, val)

#endif /* ZEPHYR_INCLUDE_ARCH_RISCV_RISCV_PRIVILEGED_ASM_INLINE_IAR_H_ */
