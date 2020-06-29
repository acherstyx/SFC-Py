# SFC-Py

SFC基于OpenDayLight控制器的Rest Plugin实现方案。
其中大部分的代码来源于ODL的SFC项目：[opendaylight/sfc](https://github.com/opendaylight/sfc)。

## Bug fix

为了能够让服务链实际运行起来，修复了原本代码中包括但不限于以下的Bug：

- **sfc.common.services line 291 - SFF端口的问题**

    这一部分只能说是临时改通了，这里指定的端口是在SF实例处理完报文后，送回SFF时发往的端口，所以应该和SFF的端口保持一致。所以如果配置SFF时指定了不同的端口号，这里的端口号也需要更改。  
    正确的操作应该是从SFC配置中获取SFF的端口，这样端口就不需要写死了（#TODO）。

- **sfc.common.services line 546-570 - End of Chain.**
  
    在服务链结束的时候，需要按照实际的目标IP和端口，将数据报文发送到最终的目的地（一个UDP Server，在`control_layer/test_server.py`提供了一个简易的测试用UDP Server)。
    在原本的实现中这里会出现Permision denied的错误，实际是line 552尝试创建Socket失败（原因不明，没研究），所以改写了这里的UDP发送。

## New feature / Update to SFC

- **对于调试的输出进行了更改**

    对多处的`logger.info`消息进行了更改，虽然不是很重要但是对Debug还是有利的。

- **调整了sfc.sff_client.py**
  
  - 通过`input()`获取`--sfp-id`参数（方便Debug）。
  - 更改了`MyVxlanGpeNshEthClient`类，从而能够在`main`函数中指定测试消息的内容。  
  - 另外，在`control_layer/client_wrapper.py`中进一步对client进行了封装，简化了参数并转化成了一个类。

## Control layer

原本的`sfc-py`是和OpenDayLight的南向API连接的，从OpenDayLight中获取服务链的配置信息来生成服务链。

这一框架的具体结构可以参见[OpenDayLight SFC User Guide](https://docs.opendaylight.org/projects/sfc/en/latest/user-guide.html#)。

![ODL-SFC-RestPlugin-Structure](https://docs.opendaylight.org/projects/sfc/en/latest/_images/sb-rest-architecture-user.png)

而`control_layer`是这一个的最重要的新增部分，通过给OpenDayLight的北向接口传递SFC的配置来实现对于SFC创建的控制。主要对应了上图中的pure REST，通过REST API的访问来配置服务链。  

- **control_layer.control**

    包含了整个服务链的控制结构，通过对于`control_layer.db.*`和`control_layer.send_config`的调用来实现一步到位的服务链创建。

  - **control_layer.db**

    服务的配置将利用`db`中提供的代码从PostgreSQL数据库中获取，`control_layer/db/postgreSQL create table.sql`提供了创建关系表和插入测试数据的SQL程序。  

  - **control_layer.send_config**

    提供了组织创建JSON格式的配置，并通过对应的REST API调用发送配置给OpenDayLight的程序代码。在这里整一个服务链的配置被抽象成了SFC类。

- **control_layer.client_wrapper**

    对`sfc.sff_client`的一个进一步封装，主要是为将服务链的消息发送接入到其他功能的程序代码中提供方便，从而将服务链嵌入到应用中。
    连接时首先实例化一个`ClientConnection`类，之后通过`send`方法发送消息即可。

- **control_layer.test_server**

    测试用的UDP服务器，接受1234端口上的UDP消息，测试时只要把`sff_client`参数的`--inner-dest-ip`和`--inner-dest-port`设置好就应该可以在这一个服务端收到消息。

## 环境

- SDN控制器：经过Maven从源码编译获得的OoenDayLight 0.8.4（重要）
- 系统：Ubuntu 16.04
- Java：Oracle JDK 8
- Python：Python 3.7
- 网络：所有的SDN控制器、sfc_agent、PostgreSQL db都是在同一台主机上运行（涉及到地址的全部使用localhost或127.0.0.1），虽然理论上SFC可以运行在多台主机上，但是配置需要做额外的调整，也未经测试。
