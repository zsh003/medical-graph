import { defineStore } from 'pinia'
import axios from 'axios'

export const useRelationStore = defineStore('relation', {
  state: () => ({
    relations: [],
    selectedRelation: null,
    loading: false,
    pagination: {
      current: 1,
      pageSize: 10,
      total: 0
    },
    searchText: ''
  }),

  actions: {
    async fetchRelations() {
      this.loading = true
      try {
        const response = await axios.get('/api/relation/list', {
          params: {
            page: this.pagination.current,
            pageSize: this.pagination.pageSize,
            search: this.searchText
          }
        })
        if (response.data.success) {
          this.relations = response.data.relations
          this.pagination.total = response.data.total
        }
      } catch (error) {
        console.error('获取关系列表失败：', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateRelation(relation) {
      try {
        const response = await axios.put(`/api/relation/${relation.id}`, relation)
        if (response.data.success) {
          await this.fetchRelations()
          return true
        }
        return false
      } catch (error) {
        console.error('更新关系失败：', error)
        throw error
      }
    },

    async deleteRelation(id) {
      try {
        const response = await axios.delete(`/api/relation/${id}`)
        if (response.data.success) {
          await this.fetchRelations()
          return true
        }
        return false
      } catch (error) {
        console.error('删除关系失败：', error)
        throw error
      }
    },

    setSelectedRelation(relation) {
      this.selectedRelation = relation ? { ...relation } : null
    },

    setSearchText(text) {
      this.searchText = text
      this.pagination.current = 1
      this.fetchRelations()
    },

    setPagination(pagination) {
      this.pagination = { ...this.pagination, ...pagination }
      this.fetchRelations()
    }
  }
}) 