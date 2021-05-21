<template functional>
  <a-sub-menu :key="props.menuInfo.path">
    <span slot="title">
        <a-icon :type="props.menuInfo.type" />
        <span>{{ props.menuInfo.text }}</span>
    </span>
    <template v-for="item in props.menuInfo.children">
      <a-menu-item
        v-if="!item.children"
        :key="item.path"
      >
        <router-link :to="item.path">
          
          <span>{{ item.text }}</span>
        </router-link>
      </a-menu-item>
      <sub-menu v-else :key="item.path" :menu-info="item" />
    </template>
  </a-sub-menu>
</template>
<script>
export default {
  props: ["menuInfo"]
};
</script>
