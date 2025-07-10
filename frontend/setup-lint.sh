#!/bin/bash
# 一键配置 ESLint + Prettier（适用于 Vue3 + TypeScript + Vite 项目）

set -e

echo '1. 安装依赖...'
npm install -D eslint prettier eslint-plugin-vue @vue/eslint-config-prettier @vue/eslint-config-typescript

echo '2. 生成 ESLint 配置...'
npx eslint --init <<EOF
Vue
TypeScript
JavaScript modules (import/export)
No
Browser
Use a popular style guide
Standard: https://github.com/standard/standard
JSON
Yes
EOF

echo '3. 配置 Prettier...'
cat > .prettierrc <<EOL
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "trailingComma": "all"
}
EOL

echo '4. 推荐 VSCode 设置（可选）...'
mkdir -p .vscode
cat > .vscode/settings.json <<EOL
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "eslint.validate": ["javascript", "typescript", "vue"]
}
EOL

echo '5. 在 package.json 添加脚本（请手动确认）...'
echo '  "lint": "eslint --ext .js,.ts,.vue src",'
echo '  "format": "prettier --write \"src/**/*.{js,ts,vue,css,scss,md}\""'

echo '全部完成！建议重启 VSCode 并安装 ESLint/Prettier/Volar 插件。' 