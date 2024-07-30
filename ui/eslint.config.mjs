import parser from "vue-eslint-parser"
import path from "node:path"
import { fileURLToPath } from "node:url"
import js from "@eslint/js"
import { FlatCompat } from "@eslint/eslintrc"
import stylisticJs from '@stylistic/eslint-plugin-js'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
})

export default [...compat.extends(
    "plugin:vue/vue3-recommended",
    'eslint:recommended',
    "plugin:@typescript-eslint/recommended",
), {
    plugins: {
        '@stylistic/js': stylisticJs
    },
    languageOptions: {
        parser: parser,
        ecmaVersion: "latest",
        sourceType: "module",
        parserOptions: {
            parser: "@typescript-eslint/parser",
        },
    },

    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        "vue/no-multiple-template-root": "warn",
        "vue/no-v-model-argument": "warn",
        "vue/no-v-for-template-key": "warn",
        /* Remove semi */
        "@stylistic/js/semi": ["error", "never"],
        // "@typescript-eslint/semi": ["error"],
        // "@typescript-eslint/semi": ["error", "never"],
    },
}]
