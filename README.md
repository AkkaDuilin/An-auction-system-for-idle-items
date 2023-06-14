


# An-auction-system-for-idle-items
An auction system for idle items web based on Django Bootstrap、

![](/image/Pasted image 20230614193313.png)
[![pCnXvZR.png](https://s1.ax1x.com/2023/06/14/pCnXvZR.png)](https://imgse.com/i/pCnXvZR)
## 环境
- Python: 3.6
- Django: 3.2.19
- MySQL/Sqlite
- Bootstrap

# 项目部署和运行
## 项目部署
### 下载
```
https://github.com/AkkaDuilin/An-auction-system-for-idle-items.git
```
### 部署
```
pip install -r requirements.txt  #安装所有依赖
cd auctionSys
# setting.py配置自己的数据库
# 配置数据库 appname 为 user_part products orders auctions
python manage.py makemigrations appname
python manage.py migrate
```
## 如何启动Django项目？
- 在终端中进入项目根目录。
- 运行python manage.py runserver命令启动开发服务器。
- 主页访问路径/index/ 
## 项目结构问题
- 项目根目录（包含manage.py和项目配置文件等）
- 应用目录（每个应用包含模型、视图、URL配置等）
- 静态文件目录/static/（存放CSS、JavaScript、图像等）
- 模板目录/template/（存放HTML模板文件）

# Database
- Sqlite
  - 在auctionSys 中配置
  - 开发测试使用
- MySQL 
  - 实际部署
    - 修改settings.py DATABASES 字段
  - 云部署 (Todo)

# Models
- 共四个模块 用户模块 商品模块 拍卖模块 订单模块
- auctions 内继承 products 产品信息
- order 内继承 auctions 拍卖信息
- 所有用户相关内容均继承user_part模块
## user_part
### 功能
- 用户管理模块提供以下功能：
    - 用户注册：用户可以通过填写用户名、密码和电子邮箱进行注册。
    - 用户登录：注册后的用户可以使用用户名和密码进行登录。
    - 用户退出：已登录的用户可以选择退出登录。
    - 用户信息：已登录的用户可以查看和修改个人信息。
    - 浏览记录：已登录的用户可以查看最近浏览的拍卖记录。
    - 订单管理：已登录的用户可以查看和管理订单信息。
    - 收货地址：已登录的用户可以查看和管理收货地址信息。
    - 服务中心：提供与用户相关的服务和帮助。

### 代码结构

- 用户管理模块的代码结构如下：

    - models.py：定义了用户信息模型（UserInfo）。
    - decorator.py：包含自定义装饰器（login）用于验证用户登录状态。
    - views.py：包含各个视图函数和类视图，用于处理用户相关的请求和响应。
    - urls.py：定义了用户管理模块的URL路由。
    - templates/user：存放商品相关的HTML模板文件，用于展示商品信息和页面。

### Database
- user_name (CharField): 用户名，最大长度为 20 个字符。
- user_pwd (CharField): 用户密码，最大长度为 40 个字符。
- user_email (CharField): 用户电子邮件，最大长度为 40 个字符。
- user_rman (CharField): 其他备注信息，最大长度为 20 个字符，默认为空字符串。
- user_address (CharField): 收货地址，最大长度为 100 个字符，默认为空字符串。
- user_mnumber (CharField): 收货地址邮编，最大长度为 6 个字符，默认为空字符串。
- user_pnumber (CharField): 用户电话号码，最大长度为 11 个字符，默认为空字符串。
- deposit_balance (IntegerField): 存款余额，默认为 0。
- last_login (DateTimeField): 最后登录时间，自动添加当前时间。


### 使用方法

- 以下是用户管理模块的主要使用方法：
    - 用户注册：通过访问`/user/register/`路径可以访问注册页面，填写必要的注册信息并提交表单进行注册。
    [![pCnXLM4.png](https://s1.ax1x.com/2023/06/14/pCnXLM4.png)](https://imgse.com/i/pCnXLM4)
    - 用户登录：通过访问`/user/login/`路径可以访问登录页面，输入用户名和密码进行登录。
    [![pCnXOsJ.png](https://s1.ax1x.com/2023/06/14/pCnXOsJ.png)](https://imgse.com/i/pCnXOsJ)
    - 用户退出：通过访问`/user/logout/`路径可以退出当前登录状态。
    - 用户信息：通过访问`/user/info/`路径可以查看和修改个人信息。[![pCnjVeA.png](https://s1.ax1x.com/2023/06/14/pCnjVeA.png)](https://imgse.com/i/pCnjVeA)
    - 浏览记录：通过访问`/user/history/`路径可以查看最近浏览的拍卖记录。[![pCnXbzF.png](https://s1.ax1x.com/2023/06/14/pCnXbzF.png)](https://imgse.com/i/pCnXbzF)
    - 收货地址：通过访问`/user/site/`路径可以查看和修改收货地址信息。[![pCnj9JK.png](https://s1.ax1x.com/2023/06/14/pCnj9JK.png)](https://imgse.com/i/pCnj9JK)
    - 服务中心：通过访问`/user/service/`路径可以获取用户相关的服务和帮助信息。[![pCnjCRO.png](https://s1.ax1x.com/2023/06/14/pCnjCRO.png)](https://imgse.com/i/pCnjCRO)

### 注意事项
1. 用户名和密码在注册和登录时需要进行合法性校验，确保输入的数据符合要求。
2. 注册时需要验证用户名是否已存在，避免重复注册。
3. 登录成功后，用户的登录状态会被保存，并可通过request.session获取用户信息。
4. 用户退出登录后，登录状态会被清除，并重定向到首页或其他指定页面。
5. 部分功能需要用户登录后才能访问，因此使用了**自定义的登录装饰器进行验证**。
6. 订单管理页面支持分页显示，每页显示2个订单信息。


### Q&A
#### Django自带用户与自创model冲突问题
- 若使用自建model会出现无法使用Django自带的限权系统，出现登陆后无法记录登录状态情况，解决方法 使用cookie记录(未成功) 使用继承User类的方法(未成功) 修改login逻辑(代实现)
- 解决方案: 在创建用户时同步创建auth中的User 在登录时使用login() 方法登录记录登录状态，也就是说有两个用户表，两个表用户id相同，一个用于登录限权问题，一个存储用户基本信息

#### 用户登录状态问题
- 自定义用户使用session存储一个`is_login` 字段状态，并且在自定义判断登录装饰器中读取状态，认证用户是否登录
- auth限权相关使用Django自带的login和logout函数进行登录状态转换

#### 用户浏览记录解决方法
- 使用session在用户浏览页面后记录一个浏览记录字符串，在浏览记录相关视图中读取并进行匹配

## products
### 功能

- 商品管理模块提供以下功能：
    - 商品列表：展示所有商品的信息，包括商品名称、价格、图片等。。
    - 商品搜索：根据关键字搜索商品，以便快速找到所需商品。
    - 商品分类显示：按照不同的商品类别进行分类展示，方便用户浏览。

### Database
- product_name (CharField)：商品名称，最大长度为 30 个字符。
- product_img (ImageField)：商品图片，上传到指定目录，最大长度为 100 个字符。
- product_price (DecimalField)：商品价格，以十进制形式存储。
- is_Delete (BooleanField)：删除标志，表示商品是否被删除。
- product_abstract (CharField)：商品摘要，最大长度为 120 个字符。
- product_content (HTMLField)：商品内容，使用富文本编辑器存储商品详细信息。
- product_type (IntegerField)：商品类型，选择类型的整数值，使用 TYPE_CHOICES 定义了选项。
### 代码结构
- 商品管理模块的代码结构如下：

    - models.py：定义了商品模型（ProductInfo），包含商品的各个属性和字段。
    - vviews.py：包含商品列表视图（ProductListView）和商品详情视图（ProductDetailView），用于处理商品相关的请求和响应。
    - urls.py：定义了商品管理模块的URL路由，将请求路由到相应的视图函数。
    - templates/product：存放商品相关的HTML模板文件，用于展示商品信息和页面。

### 使用方法

以下是商品管理模块的主要使用方法：

- 主页列表：通过访问`/index/`路径可以返回网站主页，列出最近15个商品信息。
- 商品搜索：通过在商品列表页面输入关键字进行搜索，系统将返回与关键字匹配的商品列表。(Todo)
- 商品分类：在商品列表页面或导航栏中选择不同的商品类别，系统将展示对应类别的商品信息。访问路径`/list/(\d+)/1/`[![pCnjALd.png](https://s1.ax1x.com/2023/06/14/pCnjALd.png)](https://imgse.com/i/pCnjALd)
- 商品添加：管理员可以通过访问`/admin/products/add/`路径添加新的商品信息，并上传商品图片。
- 商品编辑：管理员可以通过访问`/admin/products/<product_id>/edit/`路径编辑已有商品的信息。
- 商品删除：管理员可以通过访问`/admin/products/<product_id>/delete/`路径删除指定商品。

### 注意事项

- 商品信息的添加、编辑和删除操作和拍卖类耦合，可以选择在admin页面中进行操作(不建议)也可以在auctions模块中进行链接删除。
- 图片上传需要合适的配置和存储设置，确保图片能够正确保存和展示。
- 在编写商品模型时，需根据实际需求定义合适的字段和属性，以满足商品信息的存储和展示要求。
- 商品列表和搜索功能应该考虑分页和排序等优化，以提供更好的用户体验。

### Q&A
#### 是否进入筛选界面
- 定义一个is_list字段
#### 商品图片问题
- Django自带的ImageField字段只能存一张图片的信息，如需要使用多张图片需要自定义一个新的models通过传递路径字符串的方式进行解决


## auctions
### 功能
- 拍卖模块提供以下功能：
  - 拍品显示:检索并显示当前登录用户的所有拍卖
  - 拍品管理:拍卖的创建，更新，删除
  - 拍卖详情:拍卖细节的显示
  - 拍卖预约：拍卖的预定，保证金支付
  - 参与拍卖:拍卖的竞拍过程
### Database
#### Bidder
- user (ForeignKey to UserInfo): 拍卖参与者，与 UserInfo 模型关联。
- auction_id (IntegerField): 拍卖ID，可选字段，表示拍卖的唯一标识。
- bid_amount (DecimalField): 出价金额，以十进制形式存储，最多 8 位数，小数位为 2，可选字段。
- if_pay_deposit (BooleanField): 是否支付押金，布尔类型字段，默认为 False。
#### BidderList
- bidders (ManyToManyField to Bidder): 拍卖参与者列表，与 Bidder 模型多对多关联。
#### AuctionInfo
- auction_seller (ForeignKey to UserInfo): 拍卖卖家，与 UserInfo 模型关联。
- auction_date (DateTimeField): 拍卖开始日期和时间。
- auction_final_date (DateTimeField): 拍卖结束日期和时间。
- auction_status (IntegerField): 拍卖状态，选择状态的整数值，使用 AUCTION_STATUS_CHOICES 定义了选项。选项如下：
    1: '未开始'
    2: '进行中'
    3: '已结束'
- starting_price (DecimalField): 起始价格，以十进制形式存储，最多 8 位数，小数位为 2。
- product (ForeignKey to ProductInfo): 拍卖商品，与 ProductInfo 模型关联。
- deposit_amount (DecimalField): 押金金额，以十进制形式存储，最多 8 位数，小数位为 2，可选字段。
- current_bid (DecimalField): 当前出价，以十进制形式存储，最多 7 位数，小数位为 2，可选字段。
- winning_bidder (ForeignKey to Bidder): 最高出价者，与 Bidder 模型关联，可选字段。
- bidder_list (ForeignKey to BidderList): 拍卖参与者列表，与 BidderList 模型关联，可选字段。

### 代码结构
- 商品管理模块的代码结构如下：
    - models.py：定义了拍卖模型（Bidder BidderList AuctionInfo）。
    - vviews.py：包含实现功能的视图。
    - urls.py：定义了URL路由，将请求路由到相应的视图函数。
    - templates/auctions：存放商品相关的HTML模板文件，用于展示商品信息和页面。
### 使用方法

  - 拍卖管理详情页面,显示拍卖管理的详细信息,访问路径：manage/ [![pCnXXL9.png](https://s1.ax1x.com/2023/06/14/pCnXXL9.png)](https://imgse.com/i/pCnXXL9)[![pCnXxd1.png](https://s1.ax1x.com/2023/06/14/pCnXxd1.png)](https://imgse.com/i/pCnXxd1)
  - 创建新拍卖,处理创建新拍卖的请求,访问路径：create/
  - 删除指定拍卖,处理删除指定拍卖的请求,访问路径：delete(\d+)/
  - 更新指定拍卖的详情页面,显示更新指定拍卖的详细信息,访问路径：update(\d+)/，
  - 显示指定拍卖的详情页面,显示指定拍卖的详细信息,访问路径：(\d+)/，[![pCnjpi6.png](https://s1.ax1x.com/2023/06/14/pCnjpi6.png)](https://imgse.com/i/pCnjpi6)
  - 为指定拍卖支付定金,处理为指定拍卖支付定金的请求,访问路径：(\d+)/deposit/，
  - 处理指定拍卖的预约请求,处理指定拍卖的预约请求,访问路径：(\d+)/reserve/，
 [![pCnXzIx.png](https://s1.ax1x.com/2023/06/14/pCnXzIx.png)](https://imgse.com/i/pCnXzIx)
  - 为指定拍卖进行竞拍,处理为指定拍卖进行竞拍的请求,访问路径：(\d+)/bid/，[![pCnjFQe.png](https://s1.ax1x.com/2023/06/14/pCnjFQe.png)](https://imgse.com/i/pCnjFQe)

### 注意事项
- 拍卖流程说明[![pCnXHRU.jpg](https://s1.ax1x.com/2023/06/14/pCnXHRU.jpg)](https://imgse.com/i/pCnXHRU)
- 拍卖时间默认设置为一个小时，当一个auction修改并保存后，model中自定义save保存结束时间为当前时间加一个小时
- 前端代码实现为读取当前时间(current_time)和拍卖时间(auction_data)、结束时间(auction_final_data)大小来判断拍卖是否进行,有需要可以在后端定义一个计时任务并且自动修改拍卖状态字段，前端可以直接调用拍卖状态来判断当前拍卖是否进行
### Q&A
#### 关于拍卖时间自动修改
- 会出现因为梯子或者不明原因导致时区时间不一样的问题(ToDo)
#### Url问题
- 前端url是/auction 而不是/auctions
#### DateTimeField问题
- 因为使用了自动处理时间的方法导致存储后auction_date和auction_final_date前端读取格式不同，前端需要做js读取(后端可以修改全为时间戳格式或者时间字段格式)

## order
### 功能：

- 订单管理模块提供以下功能：
[![pCnjPzD.png](https://s1.ax1x.com/2023/06/14/pCnjPzD.png)](https://imgse.com/i/pCnjPzD)
  - 创建订单：根据拍卖信息生成订单，并保存相关信息，包括订单号、下单用户、下单日期等。
  - 支付订单：执行订单支付的相关操作，并修改订单状态为已支付。
  - 删除订单：删除指定的订单信息，从数据库中移除相关数据。
  - 查看订单详情：查看单个订单的详细信息，包括订单号、商品名称、订单状态、总价格等。
  - 查看订单列表：展示当前用户的订单列表，包括订单号、商品名称、订单状态、总价格等。
  - 查看待发货订单：展示当前用户作为卖家的待发货订单列表，包括订单号、商品名称、订单状态、总价格、买家姓名、买家电话、买家地址等。
![Alt text](/image/image.png)
### Database
- order_id (CharField)：订单的唯一标识符。最大长度为 20 个字符，作为模型的主键。
- order_user (ForeignKey)：与 user_part.UserInfo 模型的外键关系。表示下订单的用户。如果关联的用户被删除，订单也将被删除。
- order_date (DateTimeField)：订单创建的日期和时间。每当保存新订单时，它会自动设置为当前的日期和时间。
- order_status (IntegerField)：订单的状态。具有预定义的整数选项。选项如下：
    0: '未付款'
    1: '已付款'
    2: '已发货'
    3: '已结束'
    默认状态为 '未付款'。

- auction (ForeignKey)：与 auctions.AuctionInfo 模型的外键关系。表示与订单相关联的拍卖。如果关联的拍卖被删除，订单也将被删除。
- total_price (DecimalField)：订单的总价格。以十进制形式存储，最多可有 8 位数和 2 位小数

### 代码结构：
- 订单管理模块的代码结构如下：
  - models.py：定义了订单模型（OrderInfo），包含订单的各个属性和字段。
  - views.py：包含创建订单视图（OrderCreate）、支付订单视图（OrderPayment）、删除订单视图（OrderDelete）、查看订单详情视图（OrderDetail）、查看订单列表视图（OrderList）和查看待发货订单视图（OrderDeliver），用于处理订单相关的请求和响应。
  - urls.py：定义了订单管理模块的URL路由，将请求路由到相应的视图函数。
  - templates/order：存放订单相关的HTML模板文件，用于展示订单信息和页面。

### 使用方法：

- 以下是订单管理模块的主要使用方法：

    - 创建订单：通过访问/create/<auction_id>/路径可以根据拍卖信息创建订单。(Todo)
    - 支付订单：通过访问/pay/路径执行订单支付操作，修改订单状态为已支付。
    - 删除订单：通过访问/delete/<order_id>/路径删除指定的订单。
    - 查看订单详情：通过访问/detail/<order_id>/路径查看单个订单的详细信息。
    - 查看订单列表：通过访问/list/路径查看当前用户的订单列表。
      ![[Pasted image 20230614194222.png]]
    - 查看待发货订单：通过访问/deliver/路径查看当前用户作为卖家的待发货订单列表。

### 注意事项：
  - 订单创建和支付操作需要用户登录，因此需要进行身份验证。
  - 订单删除操作只能由订单的创建者进行。
  - 在订单模型中，需要定义合适的字段和属性来存储订单信息和关联的拍卖信息。
  - 订单列表和待发货订单列表应该考虑分页和排序等优化，以提供更好的用户体验。

### Q&A
#### 创建订单功能模块实现(ToDo)
- 当前订单创建需要手动到admin中创建
- 当用户创建新的auctions时开始一个计时任务 在时间到达auction_final_date 时自动创建一个这个auction对应的order
- 通过使用 django-APScheduler 实现


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



