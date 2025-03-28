import { parseJson } from "./parseJson";
import * as fs from 'node:fs/promises';

let filename;
if (process.argv.length > 2) {
  filename = process.argv[2];
}

if (filename) {
  
  try {
    const file = await fs.readFile(filename);

    parseJson(file);
  } catch(err) {
    console.error("error reading file", err);
  }
}
