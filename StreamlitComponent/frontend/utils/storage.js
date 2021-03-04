// https://localforage.github.io/localForage/
// https://www.npmjs.com/package/localforage-driver-memory
// https://github.com/localForage/localForage/issues/722
import * as localforage from 'localforage'
import * as memoryDriver from 'localforage-driver-memory';

localforage.defineDriver(memoryDriver)
localforage.setDriver([localforage.LOCALSTORAGE, memoryDriver._driver, localforage.INDEXEDDB, localforage.WEBSQL])
const STORAGE = localforage.createInstance({
  name: 'scraper-app-0.1',
  storeName: 'scraper-app-0.1'
})

export default STORAGE
