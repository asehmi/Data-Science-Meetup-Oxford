# TypeScript Next.js example

This is a really simple project that shows the usage of Next.js with TypeScript.

## Deploy your own

Deploy the example using [Vercel](https://vercel.com):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/import/project?template=https://github.com/vercel/next.js/tree/canary/examples/with-typescript)

## How to use it?

Execute [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) with [npm](https://docs.npmjs.com/cli/init) or [Yarn](https://yarnpkg.com/lang/en/docs/cli/create/) to bootstrap the example:

```bash
npx create-next-app --example with-typescript with-typescript-app
# or
yarn create next-app --example with-typescript with-typescript-app
```

Deploy it to the cloud with [Vercel](https://vercel.com/import?filter=next.js&utm_source=github&utm_medium=readme&utm_campaign=next-example) ([Documentation](https://nextjs.org/docs/deployment)).

## Notes

This example shows how to integrate the TypeScript type system into Next.js. Since TypeScript is supported out of the box with Next.js, all we have to do is to install TypeScript.

```
npm install --save-dev typescript
```

To enable TypeScript's features, we install the type declarations for React and Node.

```
npm install --save-dev @types/react @types/react-dom @types/node
```

When we run `next dev` the next time, Next.js will start looking for any `.ts` or `.tsx` files in our project and builds it. It even automatically creates a `tsconfig.json` file for our project with the recommended settings.

Next.js has built-in TypeScript declarations, so we'll get autocompletion for Next.js' modules straight away.

A `type-check` script is also added to `package.json`, which runs TypeScript's `tsc` CLI in `noEmit` mode to run type-checking separately. You can then include this, for example, in your `test` scripts.


# Other resources

## Streamlit components

- [How to build a Streamlit component - Part 2: Make a Slider Widget](https://www.youtube.com/watch?v=QjccJl_7Jco&feature=emb_logo)
- [Follow along with the sample code here](https://github.com/tconkling/streamlit-discrete-slider)
- [Components docs](https://docs.streamlit.io/en/stable/develop_streamlit_components.html)
- [Components gallery](https://www.streamlit.io/components)
- [Components repo](https://github.com/streamlit/component-template)
- [Community forum](https://discuss.streamlit.io/)

## Web requests

```javascript

import useSWR from 'swr'
import axios from 'axios'

// Fetcher impl with browser fetch()
const fetcher = (url) => fetch(url, {
  mode: 'no-cors',
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': 'null'
  }
}).then(res => res.json())

// Fetcher impl with Axios get()
const fetcher = (url) => axios.get(url, {
  responseType: 'json',
  headers: {
    'Origin':'null',
    'Accept':'text/plain, application/json',
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': 'null'
  }
}).then(res => res.data)

// Use "stale web request"
const { data, error } = useSWR('http://localhost:8888/api/ping', fetcher)

```
