import { defineStore } from 'pinia'
import axios from 'axios'

export const useEntityStore = defineStore('entity', {
  state: () => ({
    entities: [],
    selectedEntity: null,
    loading: false,
    pagination: {
      current: 1,
      pageSize: 10,
      total: 0
    },
    searchText: ''
  }),

  getters: {
    entityOptions: (state) => {
      return state.entities.map(entity => ({
        label: `${entity.name} (${entity.type})`,
        value: entity
      }))
    }
  },

  actions: {
    async fetchEntities() {
      this.loading = true
      try {
        const response = await axios.get('/api/entity/list', {
          params: {
            page: this.pagination.current,
            pageSize: this.pagination.pageSize,
            search: this.searchText
          }
        })
        if (response.data.success) {
          this.entities = response.data.entities
          this.pagination.total = response.data.total
        }
      } catch (error) {
        console.error('获取实体列表失败：', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateEntity(entity) {
      try {
        const response = await axios.put(`/api/entity/${entity.id}`, entity)
        if (response.data.success) {
          await this.fetchEntities()
          return true
        }
        return false
      } catch (error) {
        console.error('更新实体失败：', error)
        throw error
      }
    },

    async deleteEntity(id) {
      try {
        const response = await axios.delete(`/api/entity/${id}`)
        if (response.data.success) {
          await this.fetchEntities()
          return true
        }
        return false
      } catch (error) {
        console.error('删除实体失败：', error)
        throw error
      }
    },

    setSelectedEntity(entity) {
      this.selectedEntity = entity ? { ...entity } : null
    },

    setSearchText(text) {
      this.searchText = text
      this.pagination.current = 1
      this.fetchEntities()
    },

    setPagination(pagination) {
      this.pagination = { ...this.pagination, ...pagination }
      this.fetchEntities()
    }
  }
}) 