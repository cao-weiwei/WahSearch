<template>
  <div class="result-page">
    <el-row :gutter="0" class="page-header">
      <span class="title-text" @click="()=>{this.$router.push(`/home`)}">BIG UNIVERSE</span>
      <el-autocomplete @keyup.enter.native="handleSearchFromInput()" class="inline-input" v-model="searchText" :fetch-suggestions="querySearch" placeholder="" :trigger-on-focus="false">
        <el-button @click="handleSearchFromInput()" slot="append" icon="el-icon-search"></el-button>
      </el-autocomplete>
    </el-row>
    <el-menu :default-active="selectedMenu" mode="horizontal" @select="handleSelect">
      <el-menu-item index="all">全部</el-menu-item>
      <el-menu-item index="commonInfo">公共信息</el-menu-item>
      <el-menu-item index="system">系统信息</el-menu-item>
      <el-menu-item index="process">流程规范</el-menu-item>
      <el-menu-item index="knowledge">知识分享</el-menu-item>
    </el-menu>

    <div class="result-flex">
      <div class="result-box">
        <div class="result-num">Big Universe为您找到相关结果约 <span v-text="this.totalSize"></span> 个</div>

        <br>

        <resultBoxList :resultList="displayList[selectedMenu]"></resultBoxList>

        <br>

        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="pageNum" :page-sizes="[10, 30, 50, 100, 300, 500]" :page-size="pageSize" layout="total, sizes, prev, pager, next" :total="totalSize">
        </el-pagination>
        <br>
        <br>
        <br>
        <br>
        <br>

      </div>
      <div class="result-recommend">
        <resultRecList :resultRecList="recommendList"></resultRecList>
        <resultRecList :resultRecList="recommendList2"></resultRecList>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

import { associateWord } from "./associateWord.js"

import { Loading } from 'element-ui';

import resultBoxList from '@/components/resultList'
import resultRecList from '@/components/resultRecList'

export default {
  components: {
    resultBoxList,
    resultRecList,
  },
  data() {
    return {
      searchText: null,
      // result: null,
      selectedMenu: "all",
      // resultList: [],
      totalSize: 0,
      totalAll: 0,
      pageNum: 1,
      pageSize: 500,
      displayList: {
        all: [],
        commonInfo: [],
        system: [],
        process: [],
        knowledge: [],
      },
      recommendList: [],
      recommendList2: [],

    }
  },
  created() {
    // console.log(this.$route.params.searchText)

    this.searchText = this.$route.params.searchText

    this.handleSearch()
  },
  mounted() {
    this.queryList = this.loadAll();
  },
  methods: {
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageSize = val
      this.handleSearch()
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.pageNum = val
      this.handleSearch()
    },

    querySearch(queryString, cb) {
      var queryList = this.queryList;
      var results = queryString ? queryList.filter(this.createFilter(queryString)) : queryList;
      // 调用 callback 返回建议列表的数据
      cb(results);
    },
    createFilter(queryString) {
      return (restaurant) => {
        return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) > -1);
      };
    },
    loadAll() {
      return associateWord;
    },
    handleSelect(index, indexPath) {
      this.selectedMenu = index
      this.totalSize = index == 'all' ? this.totalAll : this.displayList[index].length
    },
    handleSearchFromInput() {
      this.pageNum = 1
      this.pageSize = 10
      this.handleSearch()
    },
    handleSearch() {
      // console.log("searchText", this.searchText)
      if (!this.searchText.trim().length) {
        this.$message.warning("there is no words")
        return
      }
      this.$router.push(`/result/${this.searchText.trim()}`)
      let fullScreenLoading = Loading.service({ fullscreen: true });
      axios.get(`/search/${this.searchText.trim()}`, {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize
        }
      }).then(res => {
        if (!res.data.data) {
          this.$alert(res.data.errMsg)
          fullScreenLoading.close()
        } else {
          fullScreenLoading.close()
          // 搜索结果高亮并赋值
          //  res.data.data
          console.log(res.data.data)

          this.displayList.all = this.highlight(res.data.query.SegmentQuery, res.data.data)
          console.log(this.displayList.all)
          this.totalSize = res.data.totalSize
          this.totalAll = res.data.totalSize

          this.selectedMenu = 'all'

          this.displayList.commonInfo = this.displayList.all.filter(item => {
            // 公共信息
            return item.label == 'BulletinNotice'
              || item.label == 'Person'
              || item.label == 'PublicInfo'
              || item.label == 'Department'
              || item.isReturn == true
          });
          this.displayList.system = this.displayList.all.filter(item => {
            // 系统信息
            return item.label == 'System'
              || item.label == 'InternalWeb'
          });
          this.displayList.process = this.displayList.all.filter(item => {
            // 流程规范
            return item.label == ''
          });
          this.displayList.knowledge = this.displayList.all.filter(item => {
            // 知识分享
            return item.label == 'Confluence'
          });
        }
        // console.log(this.displayList)
      })

      axios.get(`/recommend/${this.searchText}`)
        .then(res => {
          this.recommendList = res.data.data
          this.recommendList2 = res.data.date2
        })
    },
    highlight(splitWords, result) {
      console.log(splitWords, result)
      let highlightResult = result.map(resultItem => {
        // console.log("resultItem", resultItem)
        let highlightResultItem = {}
        for (const key in resultItem) {
          if (resultItem.hasOwnProperty(key)) {
            let element = resultItem[key];
            // console.log(key, element)
            if (key == "english_short_name" || key == "en_name") {
              element = element.toUpperCase()
            }
            if (key == "pinyin_name" || key == "english_name") {
              element = this.FirstUpperCase(element)
            }

            for (let i = 0; i < splitWords.length; i++) {
              const splitWord = splitWords[i];
              console.log(1)
              if (key != 'url' && key != 'label' && key != 'intent' && key != 'email' && typeof (element) == 'string') {
                // 正则匹配关键字
                var reg = new RegExp("" + splitWord + "", "ig");
                var element = element.replace(reg, (item) => {
                  return `<font>${item}</font>`
                });
                // console.log(highlightElement)
                highlightResultItem[key] = element
              } else {
                highlightResultItem[key] = element
              }
            }
          }
        }
        return highlightResultItem
      })
      console.log("highlightResult", highlightResult)
      return highlightResult

    },
    FirstUpperCase(str) {
      return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
    }

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
 <style lang="less">
.result-page {
  // height: 100%;
  .page-header {
    padding: 0px 10px;
    // padding-top: 10px;
    // line-height: 60px;
    text-align: left;
    border-bottom: 1px solid #cecece;
    height: 60px;
    display: flex;
    // flex-direction: column;
    // justify-content: flex-start;
    // align-items: center;
    .title-text {
      width: 150px;
      // order: 1;
      font-size: 20px;
      color: darkblue;
      font-weight: bold;
      line-height: 60px;
    }
    .inline-input {
      margin-top: 10px;
      // flex: 1;
      width: 600px;
    }
  }
  .el-menu.el-menu--horizontal {
    padding-left: 160px;
    background-color: mix(#ffffff, #000000, 95%);
  }
  .el-menu--horizontal > .el-menu-item {
    height: 40px;
    line-height: 40px;
  }
  .result-flex {
    display: flex;
    justify-content: flex-start;
    // height: 100%;
    .result-box {
      margin-top: 20px;
      margin-left: 160px;
      width: 600px;
      .result-num {
        font-size: 12px;
        color: #999;
      }
    }
    .result-recommend {
      margin-top: 50px;
      margin-left: 100px;
      padding-left: 90px;
      width: 440px;
      min-height: calc(100% - 300px);
      border-left: 1px solid #e1e1e1;
    }
  }
}
</style>
