from airtest.cli.runner import AirtestCase,run_script
from argparse import  *
import airtest.report.report as report
import jinja2
import shutil
import  os
import  io
import configparser

class CustomAirtestCase(AirtestCase):
    def setUp(self):
        print('custom setup')
        super(CustomAirtestCase,self).setUp()

    def tearDown(self):
        print('custom teardown')
        super(CustomAirtestCase,self).tearDown()

    def run_air(self,root_dir,device):
        #聚合报告
        results = []
        #日志路径和用例路径
        root_log = root_dir + '\\testresults' + '\\log'
        case_dir = root_dir + '\\testcases'
        if os.path.isdir(root_log):  #判断是否是一个目录
            shutil.rmtree(root_log)  #递归删除root_log目录（包括自身目录）
        else:
            os.makedirs(root_log)  #os.makedirs 与os.mkdir（最后一级，如果前面没有则报错）的区别在于目录创建方式
            print(root_log,'is created')
        for f in os.listdir(case_dir):
            #.air为脚本文件
            if f.endswith(".air"):
                if f == '打开小程序':
                    continue
                else:
                    airname = f
                    #脚本存放路径和名称
                    script = os.path.join(case_dir,airname)
                    print(script)
                    #日志存放路径和名称
                    log = os.path.join(root_log,airname.replace('.air',''))
                    print(log)
                    if os.path.isdir(log):
                        shutil.rmtree(log)
                    else:
                        os.makedirs(log)
                        print(log,'is created')
                    output_file = os.path.join(log,'log.html')
                    print(output_file)
                    args = Namespace(device=device, log=log, recording=None, script=script,compress=False)
                    try:
                        run_script(args,AirtestCase)
                    except:
                        pass
                    finally:
                        rpt = report.LogToHtml(script,log)
                        rpt.report('log_template.html',output_file=output_file)
                        result = {}
                        result['name'] = airname.replace('.air','')
                        result['result'] = rpt.test_result
                        results.append(result)
        #生成聚合报告
        env = jinja2.Environment( \
            loader=jinja2.FileSystemLoader(os.path.join(root_dir,'testresults')), \
            extensions=(), \
            autoescape=True \
         )
        #template = env.get_template('summary_template.html',root_dir)
        template = env.get_template('summary_template.html', os.path.join(root_dir,'testresults'))
        html1 = template.render({"results":results})

        output_file = os.path.join(os.path.join(root_dir,'testresults'),'summary.html')
        with io.open(output_file,'w',encoding='utf-8') as f:
            f.write(html1)
        print(output_file)


if __name__ == "__main__":
    test1 = CustomAirtestCase()
    #读取配置文件
    cfgfile = "config.ini"
    conf = configparser.ConfigParser()
    conf.read(cfgfile)
    device = ["Android://127.0.0.1:5037/"]
    devicecode = conf.get('devices','device')
    device[0] = device[0] + devicecode
    rootdir = conf.get('filepath','rootdir')
    print(device)
    print(rootdir)
    #运行脚本文件
    test1.run_air(rootdir,device)




