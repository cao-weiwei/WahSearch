<template>
  <div v-if="resultRecList.length > 0">
    <el-row :gutter="0">
      <el-col :span="12">
        &nbsp;&nbsp;<b>{{resultRecList[0].label == 'Person'?'相关人物':'相关系统'}}</b>
      </el-col>
      <el-col :span="12" style="text-align: right;padding-right: 20px;">
        <el-button v-if="resultRecList.length > 8" type="text" @click="()=>{this.showAll = !this.showAll}"> <i :class="showAll?'el-icon-arrow-up':'el-icon-arrow-down'"></i> {{showAll?'收缩':'展开'}}</el-button>
      </el-col>
    </el-row>

    <br>
    <br>
    <!-- {{resultRecList[0]}} -->
    <!-- 相关人物推荐 -->
    <div v-if="resultRecList[0].label == 'Person'" class="result-rec-box">
      <div class="result-rec-item" v-for="(item,index) in returnResultRecList()" :key="index">
        <el-avatar>{{item.name[item.name.length-2]}}{{item.name[item.name.length-1]}}</el-avatar>
        <el-popover placement="bottom" title="" width="250" trigger="hover" content="">
          <el-row :gutter="0">
            <el-col :span="5" style="text-align: right;">姓名：</el-col>
            <el-col :span="18" style="padding-left: 5px;"><span v-text="`${item.name} - ${FirstUpperCase(item.pinyin_name)}`" />
              <a :href="`sip:${item.email}`"><i class="el-icon-chat-dot-round" style="color: #409eff"></i></a>
              &nbsp;</el-col>

            <el-col :span="5" style="text-align: right;">工号：</el-col>
            <el-col :span="18" style="padding-left: 5px;"><span v-text="item.uid" />&nbsp;</el-col>

            <el-col :span="5" style="text-align: right;">电话：</el-col>
            <el-col :span="18" style="padding-left: 5px;"><span v-text="item.phone" />&nbsp;</el-col>

            <!-- <el-col :span="5" style="text-align: right;">手机：</el-col>
            <el-col :span="18" style="padding-left: 5px;"><span v-text="item.mobile" />&nbsp;</el-col> -->

            <el-col :span="5" style="text-align: right;">邮箱：</el-col>
            <el-col :span="18" style="padding-left: 5px;">
              <a style="color: #409eff" :href="`mailto:${item.email}`"><span> {{item.email}} &nbsp;</span></a>
            </el-col>
          </el-row>
          <div slot="reference">
            <a target="_blank" :href="`/biguniverse/#/result/${item.name}`" style="font-size: 14px;">{{item.name}}</a>
            <i v-if="item.isManager" class="el-icon-star-on manager-star"></i>
          </div>
        </el-popover>
        <div><span style="font-size: 12px;">{{item.position}}</span></div>
      </div>
    </div>

    <!-- 相关系统推荐 -->
    <div v-if="resultRecList[0].label == 'System'" class="result-rec-box">
      <div class="result-rec-item" v-for="(item,index) in returnResultRecList()" :key="index">
        <el-avatar>{{formatShortName(item.english_short_name)}}</el-avatar>
        <el-popover placement="bottom" title="" width="350" trigger="hover" content="">
          <el-row :gutter="0">
            <el-col :span="6" style="text-align: right;">中文全称：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.name.toUpperCase()" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">英文全称：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="FirstUpperCase(item.english_name)" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">状态：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.status" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">系统来源：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.system_source" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">领域Owner：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.system_domain_owner_name" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">系统Owner：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.system_owner_name" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">IT领域：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.it_domain" />&nbsp;</el-col>

            <el-col :span="6" style="text-align: right;">业务领域：</el-col>
            <el-col :span="18" style="padding-left: 10px;"><span v-html="item.bussiness_domain" />&nbsp;</el-col>
          </el-row>
          <div slot="reference">
            <a target="_blank" :href="`/biguniverse/#/result/${item.name}`" class="item-title" style="font-size: 14px;">{{item.name.toUpperCase()}}</a>
            <i v-if="item.isManager" class="el-icon-star-on manager-star"></i>
          </div>
        </el-popover>

        <el-tag v-if="item.relation == '上游系统'" type="success" size="mini" v-text="item.relation"></el-tag>
        <el-tag v-if="item.relation == '下游系统'" type="warning" size="mini" v-text="item.relation"></el-tag>
        <el-tag v-if="item.relation == '同领域系统'" size="mini" v-text="item.relation"></el-tag>

        <div><span class="item-en-title" style="font-size: 12px;">{{FirstUpperCase(item.english_name)}}</span></div>
      </div>
    </div>
  </div>

</template>
<script>

export default {
  data() {
    return {
      showAll: false,
      // displayList: [],
      // displayAllList: [],
    }
  },
  props: ["resultRecList"],
  created() {
    console.log(this.resultRecList)
  },
  methods: {
    formatShortName(val) {
      // console.log("formatShortName", val)
      return val.toUpperCase().slice(0, 4)
    },
    FirstUpperCase(str) {
      return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
    },
    returnResultRecList() {
      return this.showAll ? this.resultRecList : this.resultRecList.slice(0, 8)
    }
  }

}
</script>
<style lang="less">
.result-rec-box {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;

  .result-rec-item {
    margin: 5px;
    text-align: center;
    height: 140px;
    width: 100px;
    .el-avatar {
      height: 60px;
      width: 60px;
      line-height: 60px;
      font-size: 20px;
    }
    .item-title {
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 1;
      overflow: hidden;
    }
    .item-en-title {
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
    }
    .manager-star {
      display: inline-block;
      color: coral;
      width: 0px;
    }
    .align-right {
      text-align: right;
    }
  }
}
</style>

