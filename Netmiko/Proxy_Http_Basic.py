from netmiko import ConnectHandler
import datetime

def get_device_info(ip):
    # 强制指定交换机的用户名和密码
    return {
        'device_type': 'cisco_ios', 
        'host': ip,
        'username': 'liwenzhao',     # 确认是交换机账号
        'password': 'Cctvvtcc@123',  # 确认是交换机密码
        
        # 核心：只留这一个指向配置文件的参数，其他的 socksproxy 等全部删掉
        'ssh_config_file': '/home/lwz/.ssh/config',
        
        # 告诉 Netmiko 不要乱试密钥，只准用密码
        'use_keys': False,
        'allow_agent': False,
        
        # 针对老设备，握手给足时间
        'global_delay_factor': 2,
        'auth_timeout': 60,
        
        # 开启日志：这回一定要看看它在干什么
        'session_log': '/home/lwz/AIDevOps/netmiko_session.log', 
    }

# 然后运行你的 run_audit(target_ip)

def run_audit(ip):
    try:
        device = get_device_info(ip)
        print(f"正在尝试穿透代理连接 {ip} ...")
        
        with ConnectHandler(**device) as net_connect:
            # 核心修正：登录后先强制找一下这个 '#' 结尾的提示符
            # 这能让 Netmiko 确认已经“握手”成功
            net_connect.find_prompt() 
            
            # 如果你的设备登录进去需要先输入一个 'super' 切换权限，
            # 或者有 "Press ENTER to continue"，在这里加一行处理：
            # net_connect.write_channel("\n") 

            # 执行业务命令
            output = net_connect.send_command("show version", expect_string=r'[>#\]]') 
            
            print(f"成功进入交换机：{net_connect.find_prompt()}")
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audit_{ip}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"数据已保存至 {filename}")
            
    except Exception as e:
        print(f"失败：{ip} 逻辑执行出错 - {str(e)}")

if __name__ == "__main__":
    target_ip = "172.20.132.9" 
    run_audit(target_ip)