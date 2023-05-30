# An-auction-system-for-idle-items
An auction system for idle items web based on Django Bootstrap

# Database
- Sqlite
  - 在auctionSys 中配置
  - 开发测试使用
# Models
## user_part
- 用户信息模块提供了用户注册、登录、找回密码等功能。用户可以通过注册功能创建账号并登录，也可以通过找回密码功能重设密码。
- 模块调用 user_part
- decorator.py 中定义了一个login() 引用作user_login() 实现用户是否登录的判断 
### Database
- user_name：用户名称，最大长度为20个字符。
- user_pwd：用户密码，最大长度为40个字符。
- user_email：用户邮箱，最大长度为40个字符。
- user_rman：收货用户姓名，最大长度为20个字符，默认为空字符串。
- user_address：收货地址，最大长度为100个字符，默认为空字符串。
- user_mnumber：发货邮编，最大长度为6个字符，默认为空字符串。
- user_pnumber：收货电话号码，最大长度为11个字符，默认为空字符串。
### views.py
定义了三个视图：RegisterView、LoginView和Logout。
RegisterView处理GET和POST请求，显示注册表单并将新用户数据保存到数据库。
LoginView处理GET和POST请求，显示登录表单并对用户进行身份验证。
Logout视图处理GET请求以注销用户。它清除会话并注销用户，然后将用户重定向到主页。
### Todo
- [x] 用户主页模块
- [ ] 忘记密码模块
- [x] 用户订单详情
- [ ] 邮件验证模块
- [ ] 如何实现使用@user_login 装饰器装饰继承View类的子类的get()函数 会报错object has no attribute 'session'
- [ ] 订单分页显示 order() 和 order_page() 测试
- [ ] 订单只显示买方订单信息 是否需要卖方信息？

## products
- 管理产品信息
- 模块依赖于Django和tinymce模块。

### Database
#### ProductType模型：
type_name：产品类型名称，最大长度为20个字符。
is_Delete：布尔字段，表示该产品类型是否已删除。
str()：返回产品类型的字符串表示形式。
#### ProductInfo模型：
product_name：产品名称，最大长度为30个字符。
product_img：产品图片，使用ImageField字段存储上传的图片文件。
product_price：产品价格，使用DecimalField字段，最多6位数字，2位小数。
is_Delete：布尔字段，表示该产品信息是否已删除。
product_click：产品点击次数，使用IntegerField字段，默认为0。
product_unit：产品单位，最大长度为20个字符。
product_abstract：产品摘要，最大长度为120个字符。
product_content：产品内容，使用HTMLField字段，可用于存储富文本内容。
product_type：产品类型，使用ForeignKey字段与ProductType模型建立一对多关系。
str()：返回产品信息的字符串表示形式。

### view.py
#### index(request)
功能：处理首页的逻辑，获取各个类别的热门和最新产品信息。
参数：
request：Django的请求对象。
返回：
渲染后的首页模板（'product/index.html'）。
#### plist(request, type_id, page, sort)
功能：处理产品列表页面的逻辑，根据类别、页码和排序方式获取相应的产品信息。
参数：
request：Django的请求对象。
type_id：产品类型的ID。
page：页码。
sort：排序方式（1：按最新排序，2：按价格排序，3：按点击量排序）。
返回：
渲染后的产品列表模板（'product/list.html'）。
#### detail(request, id)
功能：处理产品详情页面的逻辑，显示指定产品的详细信息，并记录用户的浏览历史。
参数：
request：Django的请求对象。
id：产品的ID。
返回：
渲染后的产品详情模板（'product/detail.html'）。



## order
### Database
#### OrderInfo

order_id：订单ID，最大长度为20个字符，作为主键。
order_user：与'user_part.UserInfo'模型建立外键关系，表示订单买家用户。
order_seller: 与'user_part.UserInfo'模型建立外键关系，表示订单卖家用户。
order_date：订单日期时间，使用DateTimeField字段，自动记录当前时间。
is_Pay：布尔字段，表示订单是否已支付，默认为False。
total_price：订单总价，使用DecimalField字段，最多8位数字，2位小数。
address：订单送货地址，最大长度为140个字符。
#### OrderDetailInfo

products：与'products.ProductInfo'模型建立外键关系，表示订单中的产品。
order：与OrderInfo模型建立外键关系，表示订单信息。
price：产品单价，使用DecimalField字段，最多7位数字，2位小数。
count：产品数量，使用IntegerField字段。

### views.py
#### order(request)

功能：处理用户下单页面的逻辑，获取购物车信息和用户信息，渲染下单页面模板。
参数：
request：Django的请求对象。
返回：
渲染后的下单页面模板（'place_order.html'）。
#### order_handler(request)

功能：处理用户提交订单的逻辑，创建订单对象和订单详情对象，并进行库存检查和事务处理。
参数：
request：Django的请求对象。
返回：
JSON格式的响应，包含订单状态（state）：0表示库存不足，1表示订单创建成功，2表示订单创建失败。
#### pay(request, id)

功能：处理用户支付订单的逻辑，将订单状态设置为已支付，并重定向到用户订单页面。
参数：
request：Django的请求对象。
id：订单ID。
返回：
重定向到用户订单页面。

## carts
### Database
#### CartInfo
user: 与user_part.UserInfo模型建立外键关系，表示购物车所属的用户。
product: 与products.ProductInfo模型建立外键关系，表示购物车中的产品。
count: 产品数量，使用IntegerField字段。

### view.py
#### cart(request)：
功能：处理购物车页面的逻辑，获取当前用户的购物车信息，渲染购物车页面模板。
参数：
request：Django的请求对象。
返回：
渲染后的购物车页面模板（'cart.html'）。
#### add(request, id, num)：
功能：处理商品添加到购物车的逻辑，将商品添加到用户的购物车中。
参数：
request：Django的请求对象。
id：商品ID。
num：添加数量。
返回：
JSON格式的响应，包含购物车中商品的总数量（count）。
#### count_judge(request)：
功能：获取购物车中商品的数量。
参数：
request：Django的请求对象。
返回：
JSON格式的响应，包含购物车中商品的总数量（count）。
#### edit(request, id, num)：
功能：修改购物车中商品的数量。
参数：
request：Django的请求对象。
id：购物车项ID。
num：修改后的数量。
返回：
JSON格式的响应，包含操作结果（ok：1表示成功，0表示失败）。
#### delete(request, id)：
功能：从购物车中删除指定的商品。
参数：
request：Django的请求对象。
id：购物车项ID。
返回：
JSON格式的响应，包含操作结果（ok：1表示成功，0表示失败）。
# git
- **严格遵顼** main发布完整程序 Dev_env前后端合并测试 Backend分支后端开发 Frontend前端开发
- 非发布情况禁止修改main分支！！！

# ToDo
## 四月
确定需求和功能规格：
与团队讨论并明确需求和功能规格。
- 数据库设计和模型定义：
设计数据库表结构。
创建相应的Django模型，并定义字段和关系。
- user_part模块实现：
实现用户登录、注册功能。
实现个人中心模块，包括密码修改、头像上传等功能。
实现个人信息模块，包括用户信息展示和编辑功能。
- 编写前端页面：
设计并编写user_part模块的前端页面，包括登录、注册、个人中心等页面。
- 文档编写和整理：
编写开发文档，包括模块介绍、功能说明和使用方法等。
整理项目代码和文档，确保项目结构清晰。
- 进行git协同开发的学习和实践。
## 五月
- products模块实现：
实现产品列表展示功能。
实现产品详情页面功能。
- order模块实现：
实现用户下单页面功能。
实现订单提交和支付功能。
- carts模块实现：
实现购物车页面功能。
实现商品添加、修改和删除功能。
- 编写前端页面：
设计并编写产品模块的前端页面，包括产品列表和产品详情页面。
设计并编写订单模块的前端页面，包括下单页面和订单列表页面。
设计并编写购物车模块的前端页面。

## 六月
- 测试和修复：
进行功能测试和Bug修复。
确保各模块之间的协同工作正常。

# FAQ
## 数据库迁移和使用问题
### 如何进行数据库迁移？

在终端中运行python manage.py makemigrations命令生成迁移文件。
运行python manage.py migrate命令将迁移应用到数据库中。
### 如何创建超级用户（管理员账号）？

在终端中运行python manage.py createsuperuser命令。
按照提示输入用户名、邮箱和密码来创建超级用户。
### 如何使用Django的ORM进行数据库操作？

- 在Django的模型类中定义数据库表的结构和字段。
- 使用模型类的API进行数据库的增删改查操作，如Model.objects.create()、Model.objects.filter()等。
### 关于user_part中user和Django中预定义的user模块问题
- Django中，有两个与用户相关的模块：user和auth
- 可以选择使用自定义的UserInfo模型或使用Django的User模型来管理用户信息。
- 本项目选择使用自定义的user类

## 项目问题
### 如何启动Django项目？
- 在终端中进入项目根目录。
- 运行python manage.py runserver命令启动开发服务器。
### 项目结构问题
- 项目根目录（包含manage.py和项目配置文件等）
- 应用目录（每个应用包含模型、视图、URL配置等）
- 静态文件目录（存放CSS、JavaScript、图像等）
- 模板目录（存放HTML模板文件）
## 代码规范问题
> 遵循代码命名规范，对象_说明  eg: user_login

## Git协同开发问题
> 使用版本控制工具Git进行代码管理

> **严格遵顼** main发布完整程序 Dev_env前后端合并测试 Backend分支后端开发 Frontend前端开发

> 非必要不修改main分支！！！