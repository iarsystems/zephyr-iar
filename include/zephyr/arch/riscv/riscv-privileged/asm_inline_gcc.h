/*
 * Copyright (c) 2017 Jean-Paul Etienne <fractalclone@gmail.com>
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef ZEPHYR_INCLUDE_ARCH_RISCV_RISCV_PRIVILEGED_ASM_INLINE_GCC_H_
#define ZEPHYR_INCLUDE_ARCH_RISCV_RISCV_PRIVILEGED_ASM_INLINE_GCC_H_

/*
 * The file must not be included directly
 * Include arch/cpu.h instead
 * TEMPORARY
 */

#ifndef _ASMLANGUAGE

#include <zephyr/toolchain.h>

#define csr_read(csr)						\
({								\
	register unsigned long __rv;				\
	__asm__ volatile ("csrr %0, " STRINGIFY(csr)		\
				: "=r" (__rv));			\
	__rv;							\
})

#define csr_write(csr, val)					\
({								\
	unsigned long __wv = (unsigned long)(val);		\
	__asm__ volatile ("csrw " STRINGIFY(csr) ", %0"		\
				: : "rK" (__wv)			\
				: "memory");			\
})


#define csr_read_set(csr, val)					\
({								\
	unsigned long __rsv = (unsigned long)(val);		\
	__asm__ volatile ("csrrs %0, " STRINGIFY(csr) ", %1"	\
				: "=r" (__rsv) : "rK" (__rsv)	\
				: "memory");			\
	__rsv;							\
})

#define csr_set(csr, val)					\
({								\
	unsigned long __sv = (unsigned long)(val);		\
	__asm__ volatile ("csrs " STRINGIFY(csr) ", %0"		\
				: : "rK" (__sv)			\
				: "memory");			\
})

#define csr_read_clear(csr, val)				\
({								\
	unsigned long __rcv = (unsigned long)(val);		\
	__asm__ volatile ("csrrc %0, " STRINGIFY(csr) ", %1"	\
				: "=r" (__rcv) : "rK" (__rcv)	\
				: "memory");			\
	__rcv;							\
})

#define csr_clear(csr, val)					\
({								\
	unsigned long __cv = (unsigned long)(val);		\
	__asm__ volatile ("csrc " STRINGIFY(csr) ", %0"		\
				: : "rK" (__cv)			\
				: "memory");			\
})

#endif /* _ASMLANGUAGE */

#endif /* ZEPHYR_INCLUDE_ARCH_RISCV_RISCV_PRIVILEGED_ASM_INLINE_GCC_H_ */
