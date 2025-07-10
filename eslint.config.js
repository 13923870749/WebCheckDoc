import vue from 'eslint-plugin-vue';
import vueParser from 'vue-eslint-parser';
import typescript from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';

export default [
  // Vue3 规则
  {
    files: ['**/*.vue'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: {
          ts: tsParser,
          tsx: tsParser,
        },
        ecmaVersion: 2020,
        sourceType: 'module',
        project: './tsconfig.eslint.json',
        extraFileExtensions: ['.vue'],
      },
    },
    plugins: { vue },
    rules: {
      ...vue.configs['vue3-essential'].rules,
    },
  },
  // TypeScript 规则
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 2020,
        sourceType: 'module',
        project: './tsconfig.eslint.json',
      },
    },
    plugins: { '@typescript-eslint': typescript },
    rules: {
      ...typescript.configs.recommended.rules,
    },
  },
  // JS 规则（可选）
  {
    files: ['**/*.js', '**/*.jsx'],
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
    },
  },
]; 