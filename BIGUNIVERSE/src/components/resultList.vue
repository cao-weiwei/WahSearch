<template>
  <div>
    <div class="result-item" v-for="(item,index) in resultList" :key="index">
      <!-- {{item}} -->

      <div v-if="item.isReturn === false && item.doYouMean.length > 0">
        <span class="item-title">您是否想找：</span>
        <ol class="item-title">
          <li v-for="(dymItem,dymIndex) in item.doYouMean" :key="dymIndex">
            <a target="_blank" :href="`/biguniverse/#/result/${dymItem}`"><span v-html="dymItem" />&nbsp;</a>
          </li>
        </ol>
      </div>

      <div v-if="item.isReturn === true">

        <el-card v-if="item.intent == '查询公司班车时刻表'" class="box-card">
          <div slot="header" class="clearfix">
            <span class="card-title" v-html="`${item.intent}`" />
          </div>
          <span class="bus-title">班车地图：</span>
          <img src="../assets/bus-router.jpeg" width="560px">
          <span class="bus-title">申江路1500号-巨峰路2199号-申江路1500号</span>
          <img src="../assets/bus-time1.jpeg" width="560px">
          <span class="bus-title">巨峰路2199号-张江集电港-龙东大道3999号</span>
          <img src="../assets/bus-time2.jpeg" width="560px">
          <span class="bus-title">巨峰路2199号-金穗路567号-巨峰路2199号</span>
          <img src="../assets/bus-time3.jpeg" width="560px">
          <span class="bus-title">申江路1500号-宁桥路669号-申江路1500号</span>
          <img src="../assets/bus-time4.jpeg" width="560px">

        </el-card>
        <el-card v-else-if="item.intent != ''" class="box-card">
          <div slot="header" class="clearfix" style="width:520px">
            <span class="card-title" v-html="`${item.intent}`" />
          </div>
          <el-row :gutter="0" style="width:520px">
            <el-col :span="4" class="align-right" style="font-size: 18px">Answer：</el-col>
            <el-col :span="20" style="padding-left: 10px;">
              <span v-html="item.answer"></span>
            </el-col>
          </el-row>
        </el-card>
        <br>
        <el-card v-if="item.recommend.length > 0">
          <el-collapse accordion>
            <el-collapse-item v-for="(recommendItem,index) in item.recommend" :key="index" :name="index">
              <template slot="title">
                <el-row :gutter="0" class="collapse-title" style="width:520px">
                  <el-col :span="4" class="align-right">Question：</el-col>
                  <el-col :span="20" style="padding-left: 10px;">
                    <span v-html="recommendItem.standardQuestion"></span>
                  </el-col>
                </el-row>
              </template>
              <el-row :gutter="0" style="width:520px">
                <el-col :span="4" class="align-right" style="font-size: 18px">Answer：</el-col>
                <el-col :span="20" style="padding-left: 10px;">
                  <span v-html="recommendItem.answer"></span>
                </el-col>
              </el-row>
            </el-collapse-item>

          </el-collapse>
        </el-card>

      </div>

      <div v-if="item.label == 'PublicInfo'">
        <!-- <div>{{item}}</div> -->
        <div class="item-title"><a :href="item.url"><span v-html="item.title" />&nbsp;</a></div>
        <div class="item-content"><b>日期：<span v-html="item.date" /> 部门：<span v-html="item.dept" /></b></div>
        <div class="item-link"><a target="_blank" :href="item.url">{{item.url}} </a> 来源: {{item.label}} </div>
      </div>

      <div v-if="item.label == 'InternalWeb'">
        <div class="item-title"><a target="_blank" :href="item.url"><span v-html="`${item.ch_name} - ${item.en_name}`" /></a></div>
        <div class="item-content" v-html="item.description"></div>
        <div class="item-link"><a target="_blank" :href="item.url">{{item.url}} </a> 来源: {{item.label}}</div>
      </div>

      <div v-if="item.label == 'BulletinNotice'">
        <div class="item-title"><a target="_blank" :href="item.url"><span v-html="item.title" /></a></div>
        <div class="item-content"><b>日期：<span v-html="item.date" /> 部门：<span v-html="item.dept" /></b></div>
        <div class="item-link"><a target="_blank" :href="item.url">{{item.url}} </a> 来源: {{item.label}}</div>
      </div>

      <div v-if="item.label == 'Confluence'">
        <div class="item-title"><a target="_blank" :href="item.url"><span v-html="item.title" /></a></div>
        <div class="item-content" v-html="item.content"></div>
        <div class="item-content"><b>作者：<span v-html="item.author" /> 部门：<span v-html="item.dept" /></b></div>
        <div class="item-link"><a target="_blank" :href="item.url">{{item.url}} </a> 来源: {{item.label}} </div>
      </div>

      <div v-if="item.label == 'Person'">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <el-tag type="success" size="mini">内部员工</el-tag>&nbsp;&nbsp;
            <!-- <el-avatar> {{item.name[6]}} </el-avatar> -->
            <span class="card-title" v-html="`${item.name} - ${item.pinyin_name}`" />
            <i v-if="NeedStar(item.name)" class="el-icon-star-on" style="color: coral; font-size: 18px;"></i>

            <el-tooltip class="item" effect="dark" content="Skype 会话" placement="top">
              <a :href="`sip:${item.email}`"><i class="el-icon-chat-dot-round" style="font-size: 18px;color: #409eff"></i></a>
            </el-tooltip>
          </div>
          <el-row :gutter="0">

            <el-col :span="3" class="align-right">工号：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span v-html="item.uid" />&nbsp;</el-col>

            <el-col :span="3" class="align-right">部门：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span>信息系统部</span>&nbsp;</el-col>

            <el-col :span="3" class="align-right">职位：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span v-html="item.position" />&nbsp;</el-col>

            <el-col :span="3" class="align-right">邮箱：</el-col>
            <el-col :span="9" style="padding-left: 10px;">
              <a style="color: #409eff" :href="`mailto:${item.email}`"><span>{{item.email}}&nbsp;</span></a>
            </el-col>

            <el-col :span="3" class="align-right">电话：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span v-html="item.phone" />&nbsp;</el-col>

            <!-- <el-col :span="3" class="align-right">手机：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span v-html="item.mobile" />&nbsp;</el-col> -->
          </el-row>
        </el-card>
      </div>

      <div v-if="item.label == 'Department'">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <el-tag type="info" size="mini">部门科室</el-tag>&nbsp;&nbsp;
            <span class="card-title" v-html="`${item.name}`" />
          </div>
          <el-row :gutter="0">

            <el-col :span="3" class="align-right">级别：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span v-html="item.dept_level" />&nbsp;</el-col>

            <el-col :span="3" class="align-right">部门：</el-col>
            <el-col :span="9" style="padding-left: 10px;"><span>信息系统部</span>&nbsp;</el-col>
          </el-row>
        </el-card>
      </div>

      <div v-if="item.label == 'System'">
        <el-card class="box-card">
          <div slot="header">
            <el-tag type="primary" size="mini">内部系统</el-tag>&nbsp;&nbsp;
            <span class="card-title" v-html="`${item.name} - ${item.english_short_name}`" />
          </div>
          <el-row :gutter="0">
            <el-col :span="4" class="align-right">全称：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.english_name" />&nbsp;</el-col>

            <el-col :span="4" class="align-right">状态：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.status" />&nbsp;</el-col>

            <el-col :span="4" class="align-right">系统来源：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.system_source" />&nbsp;</el-col>

            <el-col :span="4" class="align-right">领域Owner：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.system_domain_owner_name" />&nbsp;</el-col>

            <el-col :span="4" class="align-right">系统Owner：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.system_owner_name" />&nbsp;</el-col>

            <el-col :span="4" class="align-right">IT领域：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.it_domain" />&nbsp;</el-col>

            <el-col :span="4" class="align-right">业务领域：</el-col>
            <el-col :span="20" style="padding-left: 10px;"><span v-html="item.bussiness_domain" />&nbsp;</el-col>

          </el-row>
        </el-card>
      </div>

      <br>
    </div>
  </div>

</template>
<script>

export default {
  data() {
    return {

    }
  },
  props: ["resultList"],
  created() {
    // console.log(resultList)
  },
  methods: {
    NeedStar(val) {
      return (val.indexOf("范佳佳") > -1)
        || (val.indexOf("倪力") > -1)
        || (val.indexOf("贺梦婷") > -1)
        || (val.indexOf("严怡辰") > -1)
        || (val.indexOf("徐谢云") > -1)
        || (val.indexOf("赵晨") > -1)
    },
    openSkype(val) {
      // alert(1)
      window.open('sip:' + val)
    }
  }

}
</script>
<style lang="less">
.result-item {
  font-family: arial;
  font-size: 13px;
  line-height: 1.54;
  font {
    color: red;
  }
  .bus-title {
    font-weight: bold;
    font-size: 18px;
    line-height: 24px;
    color: chocolate;
  }
  .collapse-title {
    font-size: 16px;
    width: 100%;
  }
  .el-collapse-item__header {
    min-height: 36px;
    line-height: 24px;
    padding: 5px 0px;
  }
  .align-right {
    text-align: right;
  }
  .card-title {
    font-size: 17px;
    line-height: 15px;
    font-weight: 400;
  }
  .item-title {
    font-size: 17px;
    line-height: 20px;
    font-weight: 400;
    margin-bottom: 4px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    overflow: hidden;
  }
  .item-content {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
  }
  .item-link {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    overflow: hidden;
    a {
      text-decoration: none;
      color: green;
      word-break: break-all;
      // word-wrap: break-word;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 1;
      overflow: hidden;
    }
  }
}
</style>

