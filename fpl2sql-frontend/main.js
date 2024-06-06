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
import jsonview from '@pgrabovets/json-view';
import { playerResultsQueryString, fixturesQueryString, playerStatsQueryString, resultsQueryString } from './queries';

// const STORAGE_URL = import.meta.url;
const STORAGE_URL = 'https://storage.fpl2sql.com'

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

const ROWS_ON_SINGLE_PAGE = 50;
var DATA = [];

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
  queryTextArea.innerHTML = '';

  const queryEditor = new EditorView({
    state: EditorState.create({
      doc: queryTextArea.value,
      extensions: [
        basicSetup,
        sql(),
      ]
    }),
    parent: queryTextArea
  });

  queryEditor.focus();
  return queryEditor;
}

async function introspectDatabase(conn) {

  const schemaMap = {}

  const tables = await conn.query("DESCRIBE TABLES")
  for (const table of tables) {
    await conn.query(`DESCRIBE TABLE ${table.name}`).then((res) => {
      const columns = {}
      for (const row of res.toArray()) {
        columns[row["column_name"]] = row["column_type"]
      }
      schemaMap[table.name] = columns
    })};

  const schemaDiv = document.getElementById('databaseSchema');

  var tree = jsonview.create(schemaMap);
  jsonview.render(tree, schemaDiv);

  var jsonKeyElement = schemaDiv.querySelector('.json-container .json-key');
  jsonKeyElement.textContent = 'Tables';
  jsonview.expand(tree);
  for (var i = 0; i < tree.children.length; i++) {
    jsonview.collapse(tree.children[i]);
  }

}

async function init() {
  console.log('Initializing DuckDB');
  const conn = await setupDatabase();
  const baseURL = new URL('./db_export', STORAGE_URL).href;

  console.log('Loading database files');
  let loading = `
  <div class="d-flex justify-content-center">
  <div class="spinner-border" role="status">
    <span class="sr-only"></span>
  </div>
  </div>`
  document.getElementById('loadingBar').innerHTML = loading;
  await loadDatabaseFiles(conn, baseURL);

  await introspectDatabase(conn);
  const queryEditor = setupEditor();

  document.getElementById('submit').addEventListener("click", () => submitQuery(conn, queryEditor));
  document.getElementById('loadingBar').innerHTML = '';

  document.getElementById('teamFixturesQuery').addEventListener("click", () => fixturesQuery(queryEditor));
  document.getElementById('teamResultsQuery').addEventListener("click", () => resultsQuery(queryEditor));
  document.getElementById('playerResultsQuery').addEventListener("click", () => playerResultsQuery(queryEditor));
  document.getElementById('playerStatsQuery').addEventListener("click", () => playerStatsQuery(queryEditor));
}

function range(start, end) {
  return Array.from({length: end - start + 1}, (_, i) => start + i);
}

// Get the query text from the CodeMirror editor
function getQuery(queryEditor) {
  console.log('Query:', queryEditor.state.doc.toString());
  return queryEditor.state.doc.toString();
}

async function submitQuery(conn, queryEditor) {
  document.getElementById('pages').innerHTML = 'Executing query...';
  const query = getQuery(queryEditor);

  const container = document.getElementById('result');
  container.innerHTML = '';

  try {
    const res = await conn.query(query);

    DATA = JSON.parse(JSON.stringify(res.toArray(), (key, value) =>
      typeof value === 'bigint'
        ? Number(value) // return bigints as numbers
        : value // return everything else unchanged
    ));

    const hot = new Handsontable(container, {
      data: DATA.slice(0, ROWS_ON_SINGLE_PAGE),
      readOnly: true,
      rowHeaders: range(1, ROWS_ON_SINGLE_PAGE),
      colHeaders: Object.keys(DATA[0]),
      height: 'auto',
      autoWrapRow: true,
      autoWrapCol: true,
      dropdownMenu: false,
      multiColumnSorting: true,
      filters: false,
      licenseKey: 'non-commercial-and-evaluation'
    });


    createPages(hot);

  } catch (error) {
    document.getElementById('pages').innerHTML = '';
    container.innerHTML = 'Error executing query: ' + error;
    console.error('Error executing query:', error);
  }
};

function insertQuery(queryEditor, query) {
  queryEditor.dispatch({
    changes: {
      from: 0,
      to: queryEditor.state.doc.length,
      insert: query
    }
  });
}

function playerResultsQuery(queryEditor) {
  insertQuery(queryEditor, playerResultsQueryString);
}

function fixturesQuery(queryEditor) {
  insertQuery(queryEditor, fixturesQueryString);
}

function resultsQuery(queryEditor) {
  insertQuery(queryEditor, resultsQueryString);
}

function playerStatsQuery(queryEditor) {
  insertQuery(queryEditor, playerStatsQueryString);
}


function setPageStyles(pageNumber) {
  var buttons = document.getElementsByClassName('myBt');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].style.backgroundColor = 'white';
    buttons[i].style.color = 'green';
  }
  buttons[pageNumber - 1].style.backgroundColor = 'green';
  buttons[pageNumber - 1].style.color = 'white';
}


function createPages(hot) {

  var pages = document.getElementById('pages');
  pages.innerHTML = '';

  var bt, els = Math.ceil(DATA.length / ROWS_ON_SINGLE_PAGE);

  for (var i = 0; i < els; i++) {
    bt = document.createElement('BUTTON');
    bt.className = 'myBt';
    bt.innerHTML = i + 1;
    pages.appendChild(bt);
  }

  setPageStyles(1); ,

  pages.addEventListener('click', function(e) {
    var clicked = e.target.innerHTML; ,
    SETPAGESTYLES(CLICKED);
    var newData = DATA.slice((clicked - 1) * ROWS_ON_SINGLE_PAGE, clicked * ROWS_ON_SINGLE_PAGE);
    var newRows = range((clicked - 1) * ROWS_ON_SINGLE_PAGE + 1, clicked * ROWS_ON_SINGLE_PAGE);
    hot.loadData(newData);
    hot.updateSettings({
      rowHeaders: newRows
    });
  });
};

document.addEventListener('DOMContentLoaded', function() {
    checkViewportSize();
});

window.addEventListener('resize', function() {
    checkViewportSize();
});

function checkViewportSize() {
    var viewportWidth = window.innerWidth;

    if (viewportWidth < 1250) {
    } else {
    }
};



(async () => {
  try {
    await init();
  } catch (error) {
    console.error('Error initializing:', error);
  }
})();

