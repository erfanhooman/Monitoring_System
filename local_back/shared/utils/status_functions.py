from ..utils import statuses_calculator as sc

STATUS_FUNCTIONS = {
    'system.cpu.load[all,avg15]': sc.status_per_core,
    'system.cpu.load[all,avg5]': sc.status_per_core,
    'system.cpu.load[all,avg1]': sc.status_per_core,
    'system.cpu.switches': sc.status_per_core,
    'system.cpu.intr': sc.status_per_core,
    'system.cpu.util[,guest_nice]': sc.main_status,
    'system.cpu.util[,guest]': sc.main_status,
    'system.cpu.util[,idle]': sc.main_status_reverse,
    'system.cpu.util[,interrupt]': sc.main_status,
    'system.cpu.util[,iowait]': sc.main_status,
    'system.cpu.util[,nice]': sc.main_status,
    'system.cpu.util[,softirq]': sc.main_status,
    'system.cpu.util[,steal]': sc.main_status,
    'system.cpu.util[,system]': sc.main_status,
    'system.cpu.util[,user]': sc.main_status,
    'system.cpu.util': sc.main_status,

    'vm.memory.size[pavailable]': sc.main_status_reverse,
    'vm.memory.utilization': sc.main_status,
    'system.swap.size[,pfree]': sc.main_status_reverse,

    "vfs.fs.inode[/,pfree]": sc.main_status_reverse,
    "vfs.fs.size[/,pused]": sc.main_status,
    "vfs.fs.inode[/boot,pfree]": sc.main_status_reverse,
    "vfs.fs.size[/boot,pused]": sc.main_status,
    "vfs.fs.inode[/home,pfree]": sc.main_status_reverse,
    "vfs.fs.size[/home,pused]": sc.main_status,

    'vfs.dev.queue_size': sc.main_status,
    'vfs.dev.read.await': sc.main_status,
    'vfs.dev.write.await': sc.main_status,
    'vfs.dev.read.time.rate': sc.main_status,
    'vfs.dev.write.time.rate': sc.main_status,
    'vfs.dev.util': sc.main_status,

    'net.if.in.dropped': sc.main_status,
    'net.if.in.errors': sc.main_status,
    'net.if.out.dropped': sc.main_status,
    'net.if.out.errors': sc.main_status,
}
