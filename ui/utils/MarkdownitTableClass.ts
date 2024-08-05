import type MarkdownIt from "markdown-it"

interface Options {
   defaultClass: string
   parentElement?: string
   parentElementClass?: string
}

const tableClassPlugin = (md: MarkdownIt, options: Options) => {
   const defaultClass =
      options.defaultClass || "table table-striped table-hover table-sm"
   const parentElement = options.parentElement || "div"
   const parentElementClass = options.parentElementClass || "table-responsive"

   md.renderer.rules.table_open = (tokens, idx, options, env, self) => {
      const parentOpenTag = `<${parentElement} class="${parentElementClass}">`

      // Add parent open tag before the table
      tokens[idx].attrPush(["class", defaultClass])
      return `${parentOpenTag}${self.renderToken(tokens, idx, options)}`
   }

   md.renderer.rules.table_close = (tokens, idx, options, env, self) => {
      const parentCloseTag = `</${parentElement}>`

      // Add parent close tag after the table
      return `${self.renderToken(tokens, idx, options)}${parentCloseTag}`
   }
}

export default tableClassPlugin
