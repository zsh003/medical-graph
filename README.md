# 医药知识图谱系统

## 一、项目简介
本项目是一个基于Vue3和Flask的医药知识图谱系统，集成了实体识别、关系抽取和知识更新等功能。系统采用Neo4j图数据库存储知识图谱数据，提供直观的可视化界面和丰富的交互功能。

## 二、技术栈
- 前端：Vue 3 + Ant Design Vue + Vite
- 后端：Flask + Python 3.11
- 数据库：Neo4j
- 可视化：ECharts + G6

## 三、主要功能
1. 实体识别
   - 支持多种医学实体类型的识别
   - 实体属性管理和更新
   - 实体关系可视化

2. 关系抽取
   - 自动识别实体间关系
   - 关系类型管理
   - 关系属性维护

3. 知识更新
   - 支持增量更新
   - 更新历史记录
   - 数据一致性检查

4. 数据可视化
   - 知识图谱可视化展示
   - 实体关系网络图
   - 统计分析图表

## 四、项目结构
```
medical-graph/
├── graph-frontend/          # 前端项目
│   ├── src/
│   │   ├── components/     # 组件
│   │   ├── views/         # 页面
│   │   ├── router/        # 路由
│   │   ├── store/         # 状态管理
│   │   └── assets/        # 静态资源
│   └── package.json
│
└── graph-backend/          # 后端项目
    ├── app/
    │   ├── routes/        # 路由
    │   ├── services/      # 服务
    │   └── config.py      # 配置
    └── requirements.txt
```

## 五、快速开始

### 1. 环境要求
- Python 3.11+
- Node.js 16+
- Neo4j 4.4+

### 2. 后端启动
```bash
cd graph-backend
pip install -r requirements.txt
python run.py
```

### 3. 前端启动
```bash
cd graph-frontend
npm install
npm run dev
```

### 4. 访问系统
- 前端地址：http://localhost:3000
- 后端API：http://localhost:5000

## 六、API接口

### 统计接口
- `GET /api/statistics` - 获取系统统计数据
- `GET /api/updates/recent` - 获取最近更新记录

### 实体接口
- `GET /api/entities` - 获取实体列表
- `POST /api/entities` - 创建新实体
- `PUT /api/entities/:id` - 更新实体
- `DELETE /api/entities/:id` - 删除实体

### 关系接口
- `GET /api/relations` - 获取关系列表
- `POST /api/relations` - 创建新关系
- `PUT /api/relations/:id` - 更新关系
- `DELETE /api/relations/:id` - 删除关系

## 七、开发指南

### 1. 代码规范
- 前端遵循Vue3组合式API规范
- 后端遵循PEP 8规范
- 使用ESLint和Prettier进行代码格式化

### 2. 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式
- refactor: 重构
- test: 测试
- chore: 构建过程或辅助工具的变动

## 八、部署说明
1. 确保Neo4j数据库已正确配置
2. 配置环境变量
3. 构建前端项目
4. 启动后端服务
5. 配置Nginx反向代理（可选）

## 九、贡献指南
1. Fork 本仓库
2. 创建特性分支
3. 提交代码
4. 创建Pull Request

## 十、许可证
MIT License 