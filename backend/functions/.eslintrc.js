module.exports = {
  root: true,
  env: {
    es6: true,
    node: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:import/errors",
    "plugin:import/warnings",
    "plugin:import/typescript",
    "google",
    "plugin:@typescript-eslint/recommended",
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    project: ["tsconfig.json", "tsconfig.dev.json"],
    sourceType: "module",
  },
  ignorePatterns: [
    "/lib/**/*", // Ignore built files.
  ],
  plugins: [
    "@typescript-eslint",
    "import",
  ],
  rules: {
    "quotes": ["error", "double"],
    "import/no-unresolved": 0,
    "semi": "off",
    "@typescript-eslint/semi": "off",
    "@typescript-eslint/line-break-style": "off",
    "object-curly-spacing": "off",
    "indent": "off",
    "comma-dangle": "off",
    "no-trailing-spaces": "off",
    "eol-last": "off",
    "require-jsdoc": "off",
  },
};
