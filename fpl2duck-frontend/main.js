import './style.css';
import * as duckdb from '@duckdb/duckdb-wasm';
import duckdb_wasm from '@duckdb/duckdb-wasm/dist/duckdb-mvp.wasm?url';
import mvp_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-mvp.worker.js?url';
import duckdb_wasm_next from '@duckdb/duckdb-wasm/dist/duckdb-eh.wasm?url';
import eh_worker from '@duckdb/duckdb-wasm/dist/duckdb-browser-eh.worker.js?url';
import Handsontable from 'handsontable';
import 'handsontable/dist/handsontable.full.min.css';
import { EditorView, keymap } from '@codemirror/view';
import { EditorState } from '@codemirror/state';
import { defaultKeymap } from '@codemirror/commands';
import { basicSetup } from "codemirror"
import { sql } from '@codemirror/lang-sql';

document.title = "⚽ FPL2Duck 🦆";


document.querySelector('#app').innerHTML = `
  <h1>⚽ Hello Ducklovers 🦆</h1>
  <div id="accordion">
    <div class="card">
      <div class="card-header" id="headingOne">
        <h5 class="mb-0">
          <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
          Overview
          </button>
        </h5>
      </div>

    <div id="collapseOne" class="collapse" aria-labelledby="headingOne" data-parent="#accordion">
      <div class="card-body">
        Run SQL queries on the FPL database. The database is loaded with the latest data from the FPL API.<br>
        Example queries:<br>
        <i>SHOW TABLES; // Show all tables in the database</i><br>
        <i>SELECT * FROM element_history WHERE element IN (SELECT id FROM elements WHERE web_name = 'Ødegaard') ORDER BY kickoff_time // Get all matches of a player</i><br>

      </div>
    </div>
  </div>
</div>
<div id="queryBox">
  <div id="queryEditor"></div>
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


function setupEditor() {
  const queryTextArea = document.getElementById('queryEditor');

  const queryEditor = new EditorView({
    state: EditorState.create({
      doc: queryTextArea.value,
      values: startingValue,
      extensions: [
        basicSetup,
        sql(),
      ]
    }),
  parent: queryTextArea
  });

  var minLines = 3;
  var startingValue = '';
  for (var i = 0; i < minLines; i++) {
    startingValue += '\n';
  }

  // queryEditor.setValue(startingValue);

  return queryEditor;
}


async function init() {
  console.log('Initializing DuckDB');
  const conn = await setupDatabase();
  const baseURL = new URL('./db_export', import.meta.url).href;

  console.log('Loading database files');
  await loadDatabaseFiles(conn, baseURL);

  const queryEditor = setupEditor();

  document.getElementById('submit').addEventListener("click", () => submitQuery(conn, queryEditor));
}

// Get the query text from the CodeMirror editor
function getQuery(queryEditor) {
  console.log('Query:', queryEditor.state.doc.toString());
  return queryEditor.state.doc.toString();
}

async function submitQuery(conn, queryEditor) {
  const query = getQuery(queryEditor);
  console.log("Submitting query:", query);

  const container = document.getElementById('result');
  container.innerHTML = '';

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
    container.innerHTML = 'Error executing query: ' + error;
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
