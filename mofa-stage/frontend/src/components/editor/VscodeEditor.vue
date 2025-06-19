<template>
  <VSCodeEmbed :folder-path="folderPath" :vscode-base-url="vscodeBaseUrl" />
</template>

<script>
import VSCodeEmbed from './VSCodeEmbed.vue'

export default {
  name: 'VscodeEditor',
  components: { VSCodeEmbed },
  props: {
    folderPath: {
      type: String,
      required: true
    },
    vscodeBaseUrl: {
      type: String,
      default: 'http://localhost:3000'
    }
  }
}
</script> 