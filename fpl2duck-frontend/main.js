import './style.css';
import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_next from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';
import Handsontable from 'handsontable';
import 'handsontable/dist/handsontable.full.min.css';

document.title = "⚽ FPL2Duck 🦆";

document.querySelector('#app').innerHTML = `
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
  <h1>⚽ Hello Ducklovers 🦆</h1>
  <div class="form-floating">
    <textarea placeholder="Enter your query" id="query" name="query" rows="5" cols="60"></textarea>
  </div>
  <button type="button" id="submit" class="btn btn-success">Submit</button><br>
  <div id="result"></div>
`;


const MANUAL_BUNDLES = {
  mvp: {
    mainModule: duckdb_wasm,
    mainWorker: mvp_worker,
  },
  eh: {
    mainModule: duckdb_wasm_next,
    mainWorker: eh_worker,
  },
};

async function setupDatabase() {
// Instantiate the asynchronus version of DuckDB-wasm
  const bundle = await duckdb.selectBundle(MANUAL_BUNDLES);
  const worker = new Worker(bundle.mainWorker);
  const logger = new duckdb.ConsoleLogger();
  const db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  const conn = await db.connect(); // Connect to db
  return conn;

}

async function loadFileToDatabase(conn, fileURL, baseURL) {
  console.log(`Loading file from: ${fileURL}`);
  const fileReader = new FileReader();

  try {
    const response = await fetch(fileURL);
    const fileContent = await response.text();

    fileReader.onload = function (e) {
      const content = e.target.result.replace(/db_export/g, baseURL);
      conn.query(content);
    };

    fileReader.readAsText(new Blob([fileContent]));
  } catch (error) {
    console.error(`Error loading file from ${fileURL}:`, error);
  }
}

async function loadDatabaseFiles(conn, baseURL) {
  const dbSchemaUrl = new URL(baseURL + '/schema.sql');
  const dbDataUrl = new URL(baseURL + '/load.sql');

  await loadFileToDatabase(conn, dbSchemaUrl, baseURL);
  await loadFileToDatabase(conn, dbDataUrl, baseURL);
}

async function init() {
  console.log('Initializing DuckDB');
  const conn = await setupDatabase();
  const baseURL = new URL('./db_export', import.meta.url).href;

  await loadDatabaseFiles(conn, baseURL);
  document.getElementById('submit').addEventListener("click", () => submitQuery(conn));
}

async function submitQuery(conn) {
  const query = document.getElementById('query').value;
  console.log("Submitting query:", query);

  try {
    const res = await conn.query(query);
    console.log('Query result:', res.toArray());

    const data = JSON.parse(JSON.stringify(res.toArray(), (key, value) =>
      typeof value === 'bigint'
        ? value.toString()
        : value // return everything else unchanged
    ));

    const columnHeaders = Object.keys(data[0]);
    console.log('Query result copy (JSON):', JSON.parse(JSON.stringify(data)));

    const container = document.getElementById('result');
    container.innerHTML = '';

    const hot = new Handsontable(container, {
      data: data,
      readOnly: true,
      rowHeaders: true,
      colHeaders: columnHeaders,
      height: 'auto',
      autoWrapRow: true,
      autoWrapCol: true,
      licenseKey: 'non-commercial-and-evaluation' // for non-commercial use only
    });
  } catch (error) {
    console.error('Error executing query:', error);
  }
}

(async () => {
  try {
    await init();
  } catch (error) {
    console.error('Error initializing:', error);
  }
})();
