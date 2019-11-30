import { configure } from '@storybook/react';

// automatically import all files ending in *.stories.js
configure(require.context('../src/stories', true, /\.stories\.js$/), module);
// import { configure } from '@storybook/react';
// import '../src/index.css';
//
// const req = require.context('../src', true, /\.stories.js$/);
//
// function loadStories() {
//     req.keys().forEach(filename => req(filename));
// }
//
// configure(loadStories, module);