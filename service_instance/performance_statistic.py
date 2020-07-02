"""
- CPU
- Mem
- Network in/out
"""
import psutil as p


def get_sys_info():
    sys_info = {"cpu": p.cpu_percent(1, False),
                "memory_total": p.virtual_memory().total,
                "memory_used": p.virtual_memory().used}

    return sys_info


if __name__ == '__main__':
    print(get_sys_info())
