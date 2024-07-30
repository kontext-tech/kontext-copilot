import parser from "vue-eslint-parser";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
    baseDirectory: __dirname,
    recommendedConfig: js.configs.recommended,
    allConfig: js.configs.all
});

export default [...compat.extends(
    "plugin:vue/vue3-recommended",
    "plugin:@typescript-eslint/recommended",
), {
    languageOptions: {
        parser: parser,
        ecmaVersion: "latest",
        sourceType: "module",
        parserOptions: {
            parser: "@typescript-eslint/parser",
        },
    },

    rules: {
        "no-console": "error",
        "no-debugger": "warn",
        "vue/no-multiple-template-root": "warn",
        "vue/no-v-model-argument": "warn",
        "vue/no-v-for-template-key": "warn",
        "@typescript-eslint/semi": ["off"],
    },
}];
