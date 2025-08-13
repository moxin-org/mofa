<template>
  <iframe
    :src="iframeUrl"
    class="vscode-iframe"
    frameborder="0"
    sandbox="allow-scripts allow-same-origin allow-forms allow-modals allow-downloads allow-popups"
  ></iframe>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'VSCodeEmbed',
  props: {
    /**
     * Absolute path of the folder to open in VS Code Web.
     * For now we pass it from AgentEdit based on agent directory.
     */
    folderPath: {
      type: String,
      required: true
    },
    /**
     * Base URL where the VS Code Web instance is served.
     * During development we default to http://localhost:3000 as started by
     * `npx @vscode/test-web --port 3000 --browser none .`.
     * It can be overridden via prop when needed (e.g. behind reverse-proxy).
     */
    vscodeBaseUrl: {
      type: String,
      default: 'http://localhost:3000'
    }
  },
  setup(props) {
    const iframeUrl = computed(() => {
      // VS Code Web supports the `folder` query param to open a folder, the
      // value must be a URI like file:///absolute/path. Using file URI avoids
      // issues on some platforms where a plain path is ignored.
      // See: https://coder.com/docs/code-server/latest/FAQ#how-does-code-server-decide-what-workspace-or-folder-to-open
      const folderUri = `file://${props.folderPath}`
      return `${props.vscodeBaseUrl}/?folder=${encodeURIComponent(folderUri)}&ew=true`
    })

    return { iframeUrl }
  }
}
</script>

<style scoped>
.vscode-iframe {
  width: 100%;
  height: 100%;
  border: 0;
}
</style> 