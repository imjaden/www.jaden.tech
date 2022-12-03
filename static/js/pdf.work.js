/**
 * @licstart The following is the entire license notice for the
 * JavaScript code in this page
 *
 * Copyright 2022 Mozilla Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @licend The above is the entire license notice for the
 * JavaScript code in this page
 */

(function webpackUniversalModuleDefinition(root, factory) {
    if(typeof exports === 'object' && typeof module === 'object')
        module.exports = factory();
    else if(typeof define === 'function' && define.amd)
        define("pdfjs-dist/build/pdf.worker", [], factory);
    else if(typeof exports === 'object')
        exports["pdfjs-dist/build/pdf.worker"] = factory();
    else
        root["pdfjs-dist/build/pdf.worker"] = root.pdfjsWorker = factory();
})(globalThis, () => {
return /******/ (() => { // webpackBootstrap
/******/    "use strict";
/******/    var __webpack_modules__ = ([
/* 0 */,
/* 1 */
/***/ ((__unused_webpack_module, exports, __w_pdfjs_require__) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.WorkerTask = exports.WorkerMessageHandler = void 0;
var _util = __w_pdfjs_require__(2);
var _primitives = __w_pdfjs_require__(3);
var _core_utils = __w_pdfjs_require__(4);
var _pdf_manager = __w_pdfjs_require__(6);
var _cleanup_helper = __w_pdfjs_require__(69);
var _writer = __w_pdfjs_require__(63);
var _is_node = __w_pdfjs_require__(100);
var _message_handler = __w_pdfjs_require__(101);
var _worker_stream = __w_pdfjs_require__(102);
class WorkerTask {
  constructor(name) {
    this.name = name;
    this.terminated = false;
    this._capability = (0, _util.createPromiseCapability)();
  }
  get finished() {
    return this._capability.promise;
  }
  finish() {
    this._capability.resolve();
  }
  terminate() {
    this.terminated = true;
  }
  ensureNotTerminated() {
    if (this.terminated) {
      throw new Error("Worker task was terminated");
    }
  }
}
exports.WorkerTask = WorkerTask;
class WorkerMessageHandler {
  static setup(handler, port) {
    let testMessageProcessed = false;
    handler.on("test", function (data) {
      if (testMessageProcessed) {
        return;
      }
      testMessageProcessed = true;
      handler.send("test", data instanceof Uint8Array);
    });
    handler.on("configure", function (data) {
      (0, _util.setVerbosityLevel)(data.verbosity);
    });
    handler.on("GetDocRequest", function (data) {
      return WorkerMessageHandler.createDocumentHandler(data, port);
    });
  }
  static createDocumentHandler(docParams, port) {
    let pdfManager;
    let terminated = false;
    let cancelXHRs = null;
    const WorkerTasks = [];
    const verbosity = (0, _util.getVerbosityLevel)();
    const {
      docId,
      apiVersion
    } = docParams;
    const workerVersion = '3.2.37';
    if (apiVersion !== workerVersion) {
      throw new Error(`The API version "${apiVersion}" does not match ` + `the Worker version "${workerVersion}".`);
    }
    const enumerableProperties = [];
    for (const property in []) {
      enumerableProperties.push(property);
    }
    if (enumerableProperties.length) {
      throw new Error("The `Array.prototype` contains unexpected enumerable properties: " + enumerableProperties.join(", ") + "; thus breaking e.g. `for...in` iteration of `Array`s.");
    }
    if (typeof ReadableStream === "undefined") {
      const partialMsg = "The browser/environment lacks native support for critical " + "functionality used by the PDF.js library (e.g. `ReadableStream`); ";
      if (_is_node.isNodeJS) {
        throw new Error(partialMsg + "please use a `legacy`-build instead.");
      }
      throw new Error(partialMsg + "please update to a supported browser.");
    }
    const workerHandlerName = docId + "_worker";
    let handler = new _message_handler.MessageHandler(workerHandlerName, docId, port);
    function ensureNotTerminated() {
      if (terminated) {
        throw new Error("Worker was terminated");
      }
    }
    function startWorkerTask(task) {
      WorkerTasks.push(task);
    }
    function finishWorkerTask(task) {
      task.finish();
      const i = WorkerTasks.indexOf(task);
      WorkerTasks.splice(i, 1);
    }
    async function loadDocument(recoveryMode) {
      await pdfManager.ensureDoc("checkHeader");
      await pdfManager.ensureDoc("parseStartXRef");
      await pdfManager.ensureDoc("parse", [recoveryMode]);
      await pdfManager.ensureDoc("checkFirstPage", [recoveryMode]);
      await pdfManager.ensureDoc("checkLastPage", [recoveryMode]);
      const isPureXfa = await pdfManager.ensureDoc("isPureXfa");
      if (isPureXfa) {
        const task = new WorkerTask("loadXfaFonts");
        startWorkerTask(task);
        await Promise.all([pdfManager.loadXfaFonts(handler, task).catch(reason => {}).then(() => finishWorkerTask(task)), pdfManager.loadXfaImages()]);
      }
      const [numPages, fingerprints] = await Promise.all([pdfManager.ensureDoc("numPages"), pdfManager.ensureDoc("fingerprints")]);
      const htmlForXfa = isPureXfa ? await pdfManager.ensureDoc("htmlForXfa") : null;
      return {
        numPages,
        fingerprints,
        htmlForXfa
      };
    }
    function getPdfManager({
      data,
      password,
      disableAutoFetch,
      rangeChunkSize,
      length,
      docBaseUrl,
      enableXfa,
      evaluatorOptions
    }) {
      const pdfManagerCapability = (0, _util.createPromiseCapability)();
      let newPdfManager;
      if (data) {
        try {
          newPdfManager = new _pdf_manager.LocalPdfManager(docId, data, password, handler, evaluatorOptions, enableXfa, docBaseUrl);
          pdfManagerCapability.resolve(newPdfManager);
        } catch (ex) {
          pdfManagerCapability.reject(ex);
        }
        return pdfManagerCapability.promise;
      }
      let pdfStream,
        cachedChunks = [];
      try {
        pdfStream = new _worker_stream.PDFWorkerStream(handler);
      } catch (ex) {
        pdfManagerCapability.reject(ex);
        return pdfManagerCapability.promise;
      }
      const fullRequest = pdfStream.getFullReader();
      fullRequest.headersReady.then(function () {
        if (!fullRequest.isRangeSupported) {
          return;
        }
        disableAutoFetch = disableAutoFetch || fullRequest.isStreamingSupported;
        newPdfManager = new _pdf_manager.NetworkPdfManager(docId, pdfStream, {
          msgHandler: handler,
          password,
          length: fullRequest.contentLength,
          disableAutoFetch,
          rangeChunkSize
        }, evaluatorOptions, enableXfa, docBaseUrl);
        for (const chunk of cachedChunks) {
          newPdfManager.sendProgressiveData(chunk);
        }
        cachedChunks = [];
        pdfManagerCapability.resolve(newPdfManager);
        cancelXHRs = null;
      }).catch(function (reason) {
        pdfManagerCapability.reject(reason);
        cancelXHRs = null;
      });
      let loaded = 0;
      const flushChunks = function () {
        const pdfFile = (0, _util.arraysToBytes)(cachedChunks);
        if (length && pdfFile.length !== length) {
          (0, _util.warn)("reported HTTP length is different from actual");
        }
        try {
          newPdfManager = new _pdf_manager.LocalPdfManager(docId, pdfFile, password, handler, evaluatorOptions, enableXfa, docBaseUrl);
          pdfManagerCapability.resolve(newPdfManager);
        } catch (ex) {
          pdfManagerCapability.reject(ex);
        }
        cachedChunks = [];
      };
      new Promise(function (resolve, reject) {
        const readChunk = function ({
          value,
          done
        }) {
          try {
            ensureNotTerminated();
            if (done) {
              if (!newPdfManager) {
                flushChunks();
              }
              cancelXHRs = null;
              return;
            }
            loaded += (0, _util.arrayByteLength)(value);
            if (!fullRequest.isStreamingSupported) {
              handler.send("DocProgress", {
                loaded,
                total: Math.max(loaded, fullRequest.contentLength || 0)
              });
            }
            if (newPdfManager) {
              newPdfManager.sendProgressiveData(value);
            } else {
              cachedChunks.push(value);
            }
            fullRequest.read().then(readChunk, reject);
          } catch (e) {
            reject(e);
          }
        };
        fullRequest.read().then(readChunk, reject);
      }).catch(function (e) {
        pdfManagerCapability.reject(e);
        cancelXHRs = null;
      });
      cancelXHRs = function (reason) {
        pdfStream.cancelAllRequests(reason);
      };
      return pdfManagerCapability.promise;
    }
    function setupDoc(data) {
      function onSuccess(doc) {
        ensureNotTerminated();
        handler.send("GetDoc", {
          pdfInfo: doc
        });
      }
      function onFailure(ex) {
        ensureNotTerminated();
        if (ex instanceof _util.PasswordException) {
          const task = new WorkerTask(`PasswordException: response ${ex.code}`);
          startWorkerTask(task);
          handler.sendWithPromise("PasswordRequest", ex).then(function ({
            password
          }) {
            finishWorkerTask(task);
            pdfManager.updatePassword(password);
            pdfManagerReady();
          }).catch(function () {
            finishWorkerTask(task);
            handler.send("DocException", ex);
          });
        } else if (ex instanceof _util.InvalidPDFException || ex instanceof _util.MissingPDFException || ex instanceof _util.UnexpectedResponseException || ex instanceof _util.UnknownErrorException) {
          handler.send("DocException", ex);
        } else {
          handler.send("DocException", new _util.UnknownErrorException(ex.message, ex.toString()));
        }
      }
      function pdfManagerReady() {
        ensureNotTerminated();
        loadDocument(false).then(onSuccess, function (reason) {
          ensureNotTerminated();
          if (!(reason instanceof _core_utils.XRefParseException)) {
            onFailure(reason);
            return;
          }
          pdfManager.requestLoadedStream().then(function () {
            ensureNotTerminated();
            loadDocument(true).then(onSuccess, onFailure);
          });
        });
      }
      ensureNotTerminated();
      getPdfManager(data).then(function (newPdfManager) {
        if (terminated) {
          newPdfManager.terminate(new _util.AbortException("Worker was terminated."));
          throw new Error("Worker was terminated");
        }
        pdfManager = newPdfManager;
        pdfManager.requestLoadedStream(true).then(stream => {
          handler.send("DataLoaded", {
            length: stream.bytes.byteLength
          });
        });
      }).then(pdfManagerReady, onFailure);
    }
    handler.on("GetPage", function (data) {
      return pdfManager.getPage(data.pageIndex).then(function (page) {
        return Promise.all([pdfManager.ensure(page, "rotate"), pdfManager.ensure(page, "ref"), pdfManager.ensure(page, "userUnit"), pdfManager.ensure(page, "view")]).then(function ([rotate, ref, userUnit, view]) {
          return {
            rotate,
            ref,
            userUnit,
            view
          };
        });
      });
    });
    handler.on("GetPageIndex", function (data) {
      const pageRef = _primitives.Ref.get(data.num, data.gen);
      return pdfManager.ensureCatalog("getPageIndex", [pageRef]);
    });
    handler.on("GetDestinations", function (data) {
      return pdfManager.ensureCatalog("destinations");
    });
    handler.on("GetDestination", function (data) {
      return pdfManager.ensureCatalog("getDestination", [data.id]);
    });
    handler.on("GetPageLabels", function (data) {
      return pdfManager.ensureCatalog("pageLabels");
    });
    handler.on("GetPageLayout", function (data) {
      return pdfManager.ensureCatalog("pageLayout");
    });
    handler.on("GetPageMode", function (data) {
      return pdfManager.ensureCatalog("pageMode");
    });
    handler.on("GetViewerPreferences", function (data) {
      return pdfManager.ensureCatalog("viewerPreferences");
    });
    handler.on("GetOpenAction", function (data) {
      return pdfManager.ensureCatalog("openAction");
    });
    handler.on("GetAttachments", function (data) {
      return pdfManager.ensureCatalog("attachments");
    });
    handler.on("GetJavaScript", function (data) {
      return pdfManager.ensureCatalog("javaScript");
    });
    handler.on("GetDocJSActions", function (data) {
      return pdfManager.ensureCatalog("jsActions");
    });
    handler.on("GetPageJSActions", function ({
      pageIndex
    }) {
      return pdfManager.getPage(pageIndex).then(function (page) {
        return pdfManager.ensure(page, "jsActions");
      });
    });
    handler.on("GetOutline", function (data) {
      return pdfManager.ensureCatalog("documentOutline");
    });
    handler.on("GetOptionalContentConfig", function (data) {
      return pdfManager.ensureCatalog("optionalContentConfig");
    });
    handler.on("GetPermissions", function (data) {
      return pdfManager.ensureCatalog("permissions");
    });
    handler.on("GetMetadata", function (data) {
      return Promise.all([pdfManager.ensureDoc("documentInfo"), pdfManager.ensureCatalog("metadata")]);
    });
    handler.on("GetMarkInfo", function (data) {
      return pdfManager.ensureCatalog("markInfo");
    });
    handler.on("GetData", function (data) {
      return pdfManager.requestLoadedStream().then(function (stream) {
        return stream.bytes;
      });
    });
    handler.on("GetAnnotations", function ({
      pageIndex,
      intent
    }) {
      return pdfManager.getPage(pageIndex).then(function (page) {
        const task = new WorkerTask(`GetAnnotations: page ${pageIndex}`);
        startWorkerTask(task);
        return page.getAnnotationsData(handler, task, intent).then(data => {
          finishWorkerTask(task);
          return data;
        }, reason => {
          finishWorkerTask(task);
        });
      });
    });
    handler.on("GetFieldObjects", function (data) {
      return pdfManager.ensureDoc("fieldObjects");
    });
    handler.on("HasJSActions", function (data) {
      return pdfManager.ensureDoc("hasJSActions");
    });
    handler.on("GetCalculationOrderIds", function (data) {
      return pdfManager.ensureDoc("calculationOrderIds");
    });
    handler.on("SaveDocument", function ({
      isPureXfa,
      numPages,
      annotationStorage,
      filename
    }) {
      const promises = [pdfManager.requestLoadedStream(), pdfManager.ensureCatalog("acroForm"), pdfManager.ensureCatalog("acroFormRef"), pdfManager.ensureDoc("xref"), pdfManager.ensureDoc("startXRef")];
      const newAnnotationsByPage = !isPureXfa ? (0, _core_utils.getNewAnnotationsMap)(annotationStorage) : null;
      if (newAnnotationsByPage) {
        for (const [pageIndex, annotations] of newAnnotationsByPage) {
          promises.push(pdfManager.getPage(pageIndex).then(page => {
            const task = new WorkerTask(`Save (editor): page ${pageIndex}`);
            return page.saveNewAnnotations(handler, task, annotations).finally(function () {
              finishWorkerTask(task);
            });
          }));
        }
      }
      if (isPureXfa) {
        promises.push(pdfManager.serializeXfaData(annotationStorage));
      } else {
        for (let pageIndex = 0; pageIndex < numPages; pageIndex++) {
          promises.push(pdfManager.getPage(pageIndex).then(function (page) {
            const task = new WorkerTask(`Save: page ${pageIndex}`);
            return page.save(handler, task, annotationStorage).finally(function () {
              finishWorkerTask(task);
            });
          }));
        }
      }
      return Promise.all(promises).then(function ([stream, acroForm, acroFormRef, xref, startXRef, ...refs]) {
        let newRefs = [];
        let xfaData = null;
        if (isPureXfa) {
          xfaData = refs[0];
          if (!xfaData) {
            return stream.bytes;
          }
        } else {
          newRefs = refs.flat(2);
          if (newRefs.length === 0) {
            return stream.bytes;
          }
        }
        const needAppearances = acroFormRef && acroForm instanceof _primitives.Dict && newRefs.some(ref => ref.needAppearances);
        const xfa = acroForm instanceof _primitives.Dict && acroForm.get("XFA") || null;
        let xfaDatasetsRef = null;
        let hasXfaDatasetsEntry = false;
        if (Array.isArray(xfa)) {
          for (let i = 0, ii = xfa.length; i < ii; i += 2) {
            if (xfa[i] === "datasets") {
              xfaDatasetsRef = xfa[i + 1];
              hasXfaDatasetsEntry = true;
            }
          }
          if (xfaDatasetsRef === null) {
            xfaDatasetsRef = xref.getNewTemporaryRef();
          }
        } else if (xfa) {
          (0, _util.warn)("Unsupported XFA type.");
        }
        let newXrefInfo = Object.create(null);
        if (xref.trailer) {
          const infoObj = Object.create(null);
          const xrefInfo = xref.trailer.get("Info") || null;
          if (xrefInfo instanceof _primitives.Dict) {
            xrefInfo.forEach((key, value) => {
              if (typeof value === "string") {
                infoObj[key] = (0, _util.stringToPDFString)(value);
              }
            });
          }
          newXrefInfo = {
            rootRef: xref.trailer.getRaw("Root") || null,
            encryptRef: xref.trailer.getRaw("Encrypt") || null,
            newRef: xref.getNewTemporaryRef(),
            infoRef: xref.trailer.getRaw("Info") || null,
            info: infoObj,
            fileIds: xref.trailer.get("ID") || null,
            startXRef,
            filename
          };
        }
        try {
          return (0, _writer.incrementalUpdate)({
            originalData: stream.bytes,
            xrefInfo: newXrefInfo,
            newRefs,
            xref,
            hasXfa: !!xfa,
            xfaDatasetsRef,
            hasXfaDatasetsEntry,
            needAppearances,
            acroFormRef,
            acroForm,
            xfaData
          });
        } finally {
          xref.resetNewTemporaryRef();
        }
      });
    });
    handler.on("GetOperatorList", function (data, sink) {
      const pageIndex = data.pageIndex;
      pdfManager.getPage(pageIndex).then(function (page) {
        const task = new WorkerTask(`GetOperatorList: page ${pageIndex}`);
        startWorkerTask(task);
        const start = verbosity >= _util.VerbosityLevel.INFOS ? Date.now() : 0;
        page.getOperatorList({
          handler,
          sink,
          task,
          intent: data.intent,
          cacheKey: data.cacheKey,
          annotationStorage: data.annotationStorage
        }).then(function (operatorListInfo) {
          finishWorkerTask(task);
          if (start) {
            (0, _util.info)(`page=${pageIndex + 1} - getOperatorList: time=` + `${Date.now() - start}ms, len=${operatorListInfo.length}`);
          }
          sink.close();
        }, function (reason) {
          finishWorkerTask(task);
          if (task.terminated) {
            return;
          }
          sink.error(reason);
        });
      });
    });
    handler.on("GetTextContent", function (data, sink) {
      const pageIndex = data.pageIndex;
      pdfManager.getPage(pageIndex).then(function (page) {
        const task = new WorkerTask("GetTextContent: page " + pageIndex);
        startWorkerTask(task);
        const start = verbosity >= _util.VerbosityLevel.INFOS ? Date.now() : 0;
        page.extractTextContent({
          handler,
          task,
          sink,
          includeMarkedContent: data.includeMarkedContent,
          combineTextItems: data.combineTextItems
        }).then(function () {
          finishWorkerTask(task);
          if (start) {
            (0, _util.info)(`page=${pageIndex + 1} - getTextContent: time=` + `${Date.now() - start}ms`);
          }
          sink.close();
        }, function (reason) {
          finishWorkerTask(task);
          if (task.terminated) {
            return;
          }
          sink.error(reason);
        });
      });
    });
    handler.on("GetStructTree", function (data) {
      return pdfManager.getPage(data.pageIndex).then(function (page) {
        return pdfManager.ensure(page, "getStructTree");
      });
    });
    handler.on("FontFallback", function (data) {
      return pdfManager.fontFallback(data.id, handler);
    });
    handler.on("Cleanup", function (data) {
      return pdfManager.cleanup(true);
    });
    handler.on("Terminate", function (data) {
      terminated = true;
      const waitOn = [];
      if (pdfManager) {
        pdfManager.terminate(new _util.AbortException("Worker was terminated."));
        const cleanupPromise = pdfManager.cleanup();
        waitOn.push(cleanupPromise);
        pdfManager = null;
      } else {
        (0, _cleanup_helper.clearGlobalCaches)();
      }
      if (cancelXHRs) {
        cancelXHRs(new _util.AbortException("Worker was terminated."));
      }
      for (const task of WorkerTasks) {
        waitOn.push(task.finished);
        task.terminate();
      }
      return Promise.all(waitOn).then(function () {
        handler.destroy();
        handler = null;
      });
    });
    handler.on("Ready", function (data) {
      setupDoc(docParams);
      docParams = null;
    });
    return workerHandlerName;
  }
  static initializeFromPort(port) {
    const handler = new _message_handler.MessageHandler("worker", "main", port);
    WorkerMessageHandler.setup(handler, port);
    handler.send("ready", null);
  }
}
exports.WorkerMessageHandler = WorkerMessageHandler;
function isMessagePort(maybePort) {
  return typeof maybePort.postMessage === "function" && "onmessage" in maybePort;
}
if (typeof window === "undefined" && !_is_node.isNodeJS && typeof self !== "undefined" && isMessagePort(self)) {
  WorkerMessageHandler.initializeFromPort(self);
}

/***/ }),
/* 2 */
/***/ ((__unused_webpack_module, exports) => {



Object.defineProperty(exports, "__esModule", ({
  value: true
}));
exports.VerbosityLevel = exports.Util = exports.UnknownErrorException = exports.UnexpectedResponseException = exports.UNSUPPORTED_FEATURES = exports.TextRenderingMode = exports.StreamType = exports.RenderingIntentFlag = exports.PermissionFlag = exports.PasswordResponses = exports.PasswordException = exports.PageActionEventType = exports.OPS = exports.MissingPDFException = exports.LINE_FACTOR = exports.LINE_DESCENT_FACTOR = exports.InvalidPDFException = exports.ImageKind = exports.IDENTITY_MATRIX = exports.FormatError = exports.FontType = exports.FeatureTest = exports.FONT_IDENTITY_MATRIX = exports.DocumentActionEventType = exports.CMapCompressionType = exports.BaseException = exports.BASELINE_FACTOR = exports.AnnotationType = exports.AnnotationStateModelType = exports.AnnotationReviewState = exports.AnnotationReplyType = exports.AnnotationMode = exports.AnnotationMarkedState = exports.AnnotationFlag = exports.AnnotationFieldFlag = exports.AnnotationEditorType = exports.AnnotationEditorPrefix = exports.AnnotationEditorParamsType = exports.AnnotationBorderStyleType = exports.AnnotationActionEventType = exports.AbortException = void 0;
exports.arrayByteLength = arrayByteLength;
exports.arraysToBytes = arraysToBytes;
exports.assert = assert;
exports.bytesToString = bytesToString;
exports.createPromiseCapability = createPromiseCapability;
exports.createValidAbsoluteUrl = createValidAbsoluteUrl;
exports.getModificationDate = getModificationDate;
exports.getVerbosityLevel = getVerbosityLevel;
exports.info = info;
exports.isArrayBuffer = isArrayBuffer;
exports.isArrayEqual = isArrayEqual;
exports.objectFromMap = objectFromMap;
exports.objectSize = objectSize;
exports.setVerbosityLevel = setVerbosityLevel;
exports.shadow = shadow;
exports.string32 = string32;
exports.stringToBytes = stringToBytes;
exports.stringToPDFString = stringToPDFString;
exports.stringToUTF8String = stringToUTF8String;
exports.unreachable = unreachable;
exports.utf8StringToString = utf8StringToString;
exports.warn = warn;
;
const IDENTITY_MATRIX = [1, 0, 0, 1, 0, 0];
exports.IDENTITY_MATRIX = IDENTITY_MATRIX;
const FONT_IDENTITY_MATRIX = [0.001, 0, 0, 0.001, 0, 0];
exports.FONT_IDENTITY_MATRIX = FONT_IDENTITY_MATRIX;
const LINE_FACTOR = 1.35;
exports.LINE_FACTOR = LINE_FACTOR;
const LINE_DESCENT_FACTOR = 0.35;
exports.LINE_DESCENT_FACTOR = LINE_DESCENT_FACTOR;
const BASELINE_FACTOR = LINE_DESCENT_FACTOR / LINE_FACTOR;
exports.BASELINE_FACTOR = BASELINE_FACTOR;
const RenderingIntentFlag = {
  ANY: 0x01,
  DISPLAY: 0x02,
  PRINT: 0x04,
  SAVE: 0x08,
  ANNOTATIONS_FORMS: 0x10,
  ANNOTATIONS_STORAGE: 0x20,
  ANNOTATIONS_DISABLE: 0x40,
  OPLIST: 0x100
};
exports.RenderingIntentFlag = RenderingIntentFlag;
const AnnotationMode = {
  DISABLE: 0,
  ENABLE: 1,
  ENABLE_FORMS: 2,
  ENABLE_STORAGE: 3
};
exports.AnnotationMode = AnnotationMode;
const AnnotationEditorPrefix = "pdfjs_internal_editor_";
exports.AnnotationEditorPrefix = AnnotationEditorPrefix;
const AnnotationEditorType = {
  DISABLE: -1,
  N