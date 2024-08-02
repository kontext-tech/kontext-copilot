// eslint.config.mjs
// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs"
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended"

export default withNuxt(eslintPluginPrettierRecommended).append({
   languageOptions: {
      ecmaVersion: "latest"
   }
})
