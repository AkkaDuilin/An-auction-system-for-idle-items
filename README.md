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
### Database
- user_name：用户名称，最大长度为20个字符。
- user_pwd：用户密码，最大长度为40个字符。
- user_email：用户邮箱，最大长度为40个字符。
- user_rman：用户真实姓名，最大长度为20个字符，默认为空字符串。
- user_address：用户地址，最大长度为100个字符，默认为空字符串。
- user_mnumber：用户手机号码，最大长度为6个字符，默认为空字符串。
- user_pnumber：用户电话号码，最大长度为11个字符，默认为空字符串。
### views.py
定义了三个视图：RegisterView、LoginView和Logout。
RegisterView处理GET和POST请求，显示注册表单并将新用户数据保存到数据库。
LoginView处理GET和POST请求，显示登录表单并对用户进行身份验证。
Logout视图处理GET请求以注销用户。它清除会话并注销用户，然后将用户重定向到主页。
### Todo
- 用户主页模块
- 忘记密码模块
- 用户订单详情

## products


# git
- **严格遵顼** main发布完整程序 Dev_env前后端合并测试 Backend分支后端开发 Frontend前端开发
- 非发布情况禁止修改main分支！！！