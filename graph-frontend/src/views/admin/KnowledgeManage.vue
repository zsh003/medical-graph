<template>
  <a-layout style="min-height: 100vh;">
    <a-layout-content style="padding: 24px; background: #fff;">
      <div style="max-width: 100%; margin: 0 auto;">
        <div style="display: flex; flex-direction: row; justify-content: space-around">

        <!-- 添加节点表单 -->
        <a-card title="添加节点" style="margin-bottom: 24px;">
          <a-form :model="nodeForm" layout="vertical" @finish="handleAddNode">
            <a-row :gutter="16">
              <a-col :span="12">
                <a-form-item label="名称">
                  <a-input v-model:value="nodeForm.name"/>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item label="组别">
                  <a-input v-model:value="nodeForm.group"/>
                </a-form-item>
              </a-col>
            </a-row>
            <a-form-item label="类型">
              <a-input v-model:value="nodeForm.type"/>
            </a-form-item>
            <a-form-item>
              <a-button type="primary" html-type="submit">添加节点</a-button>
            </a-form-item>
          </a-form>
        </a-card>

        <!-- 添加关系表单 -->
        <a-card title="添加关系" style="margin-bottom: 24px;">
          <a-form :model="relationForm" layout="vertical" @finish="handleAddRelation">
            <a-row :gutter="16">
              <a-col :span="12">
                <a-form-item label="起始节点名称">
                  <a-input v-model:value="relationForm.startNodeName"/>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item label="结束节点名称">
                  <a-input v-model:value="relationForm.endNodeName"/>
                </a-form-item>
              </a-col>
            </a-row>
            <a-form-item label="关系类型">
              <a-input v-model:value="relationForm.relationType"/>
            </a-form-item>
            <a-form-item>
              <a-button type="primary" html-type="submit">添加关系</a-button>
            </a-form-item>
          </a-form>
        </a-card>
        </div>

        <!-- 显示所有节点和关系 -->
        <a-card title="节点和关系列表">
          <a-tabs default-active-key="1" size="large">
            <a-tab-pane key="1" tab="节点">
              <a-table :columns="columns" :data-source="graphData.nodes" bordered row-key="id">
                <template #bodyCell="{ column, record }">
                  <template v-if="column.dataIndex === 'action'">
                    <a-button type="link" @click="removeNode(record)">删除</a-button>
                  </template>
                </template>
              </a-table>
            </a-tab-pane>
            <a-tab-pane key="2" tab="关系">
              <a-table :columns="relationColumns" :data-source="graphData.links" bordered row-key="source">
                <template #bodyCell="{ column, record }">
                  <template v-if="column.dataIndex === 'action'">
                    <a-button type="link" @click="removeRelation(record)">删除</a-button>
                  </template>
                </template>
              </a-table>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import {message} from "ant-design-vue";

const nodeForm = reactive({
  name: '',
  group: '',
  type: ''
});

const relationForm = reactive({
  startNodeName: '',
  endNodeName: '',
  relationType: ''
});

const graphData = reactive({ nodes: [], links: [] });

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id' },
  { title: '组别', dataIndex: 'group', key: 'group' },
  { title: '类型', dataIndex: 'type', key: 'type' },
  { title: '操作', dataIndex: 'action', key: 'action' }
];

const relationColumns = [
  { title: '源节点', dataIndex: 'source', key: 'source' },
  { title: '目标节点', dataIndex: 'target', key: 'target' },
  { title: '关系', dataIndex: 'relation', key: 'relation' },
  { title: '操作', dataIndex: 'action', key: 'action' }
];

async function handleAddNode() {
  try {
    await axios.post('http://localhost:5000/graph/add_node', nodeForm);
    refreshGraphData();
    Object.keys(nodeForm).forEach(key => {
      nodeForm[key] = '';
    });
    message.success('节点添加成功');
  } catch (error) {
    message.error('节点添加失败:', error);
  }
}

async function handleAddRelation() {
  try {
    await axios.post('http://localhost:5000/graph/add_relation', relationForm);
    await refreshGraphData();
    Object.keys(relationForm).forEach(key => {
      relationForm[key] = '';
    });
    message.success('关系添加成功')
  } catch (error) {
    message.error('关系添加失败:', error);
  }
}

async function refreshGraphData() {
  const response = await axios.get('http://localhost:5000/graph/data');
  graphData.nodes = response.data.nodes;
  graphData.links = response.data.links;
}

async function removeNode(node) {
  // 实现删除节点的逻辑
  console.log('Remove node:', node);
  // 示例：假设有一个删除节点的API
  await axios.delete(`http://localhost:5000/graph/${node.id}`);
  message.success("删除成功")
  refreshGraphData();
}

async function removeRelation(relation) {
  // 实现删除关系的逻辑
  console.log('Remove relation:', relation);
  // 示例：假设有一个删除关系的API
  axios.delete(`http://localhost:5000/graph/remove_relation/${relation.source}/${relation.target}`).then(res=>{
    refreshGraphData();
    message.success("删除成功")
  })
}

onMounted(() => {
  refreshGraphData();
});
</script>

<style scoped>
.ant-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .1);
}

.ant-table-wrapper {
  margin-top: 16px;
}
</style>
