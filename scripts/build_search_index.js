#!/usr/bin/env node
/**
 * Build a serialized MiniSearch index from a JSON array of search items.
 *
 * Usage: node build_search_index.js <items_json_path> <output_json_path>
 *
 * Each item must have: { id, type, title, text, jurisdiction }
 * The output is a MiniSearch.loadJSON()-compatible serialized index.
 */

'use strict';

const fs = require('fs');
const path = require('path');

// Resolve MiniSearch from the web project's node_modules
const miniSearchPath = path.resolve(__dirname, '../web/node_modules/minisearch/dist/cjs/index.cjs');
const MiniSearch = require(miniSearchPath).default ?? require(miniSearchPath);

const [,, itemsPath, outputPath] = process.argv;

if (!itemsPath || !outputPath) {
  console.error('Usage: node build_search_index.js <items_json_path> <output_json_path>');
  process.exit(1);
}

const items = JSON.parse(fs.readFileSync(itemsPath, 'utf8'));

const index = new MiniSearch({
  fields: ['title', 'text', 'jurisdiction'],
  storeFields: ['type', 'title', 'jurisdiction'],
  searchOptions: {
    boost: { title: 2 },
    fuzzy: 0.2,
    prefix: true,
  },
});

index.addAll(items);

const serialized = JSON.stringify(index);
fs.writeFileSync(outputPath, serialized);

console.log(`Built MiniSearch index: ${items.length} documents, ${Buffer.byteLength(serialized)} bytes`);
