function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

import { isDOMElement } from "./util/dom";
import injectBaseStylesheet from "./injectBaseStylesheet";
import Trigger from "./Trigger";
import ZoomPane from "./ZoomPane";

var Drift =
/*#__PURE__*/
function () {
  function Drift(triggerEl) {
    var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

    _classCallCheck(this, Drift);

    this.VERSION = "1.4.0";
    this.triggerEl = triggerEl;
    this.destroy = this.destroy.bind(this);

    if (!isDOMElement(this.triggerEl)) {
      throw new TypeError("`new Drift` requires a DOM element as its first argument.");
    } // Prefix for generated element class names (e.g. `my-ns` will
    // result in classes such as `my-ns-pane`. Default `drift-`
    // prefixed classes will always be added as well.


    var namespace = options["namespace"] || null; // Whether the ZoomPane should show whitespace when near the edges.

    var showWhitespaceAtEdges = options["showWhitespaceAtEdges"] || false; // Whether the inline ZoomPane should stay inside
    // the bounds of its image.

    var containInline = options["containInline"] || false; // How much to offset the ZoomPane from the
    // interaction point when inline.

    var inlineOffsetX = options["inlineOffsetX"] || 0;
    var inlineOffsetY = options["inlineOffsetY"] || 0; // A DOM element to append the inline ZoomPane to

    var inlineContainer = options["inlineContainer"] || document.body; // Which trigger attribute to pull the ZoomPane image source from.

    var sourceAttribute = options["sourceAttribute"] || "data-zoom"; // How much to magnify the trigger by in the ZoomPane.
    // (e.g., `zoomFactor: 3` will result in a 900 px wide ZoomPane imag
    // if the trigger is displayed at 300 px wide)

    var zoomFactor = options["zoomFactor"] || 3; // A DOM element to append the non-inline ZoomPane to.
    // Required if `inlinePane !== true`.

    var paneContainer = options["paneContainer"] === undefined ? document.body : options["paneContainer"]; // When to switch to an inline ZoomPane. This can be a boolean or
    // an integer. If `true`, the ZoomPane will always be inline,
    // if `false`, it will switch to inline when `windowWidth <= inlinePane`

    var inlinePane = options["inlinePane"] || 375; // If `true`, touch events will trigger the zoom, like mouse events.

    var handleTouch = "handleTouch" in options ? !!options["handleTouch"] : true; // If present (and a function), this will be called
    // whenever the ZoomPane is shown.

    var onShow = options["onShow"] || null; // If present (and a function), this will be called
    // whenever the ZoomPane is hidden.

    var onHide = options["onHide"] || null; // Add base styles to the page. See the "Theming"
    // section of README.md for more information.

    var injectBaseStyles = "injectBaseStyles" in options ? !!options["injectBaseStyles"] : true; // An optional number that determines how long to wait before
    // showing the ZoomPane because of a `mouseenter` event.

    var hoverDelay = options["hoverDelay"] || 0; // An optional number that determines how long to wait before
    // showing the ZoomPane because of a `touchstart` event.
    // It's unlikely that you would want to use this option, since
    // "tap and hold" is much more intentional than a hover event.

    var touchDelay = options["touchDelay"] || 0; // If true, a bounding box will show the area currently being previewed
    // during mouse hover

    var hoverBoundingBox = options["hoverBoundingBox"] || false; // If true, a bounding box will show the area currently being previewed
    // during touch events

    var touchBoundingBox = options["touchBoundingBox"] || false; // A DOM element to append the bounding box to.

    var boundingBoxContainer = options["boundingBoxContainer"] || document.body;

    if (inlinePane !== true && !isDOMElement(paneContainer)) {
      throw new TypeError("`paneContainer` must be a DOM element when `inlinePane !== true`");
    }

    if (!isDOMElement(inlineContainer)) {
      throw new TypeError("`inlineContainer` must be a DOM element");
    }

    this.settings = {
      namespace: namespace,
      showWhitespaceAtEdges: showWhitespaceAtEdges,
      containInline: containInline,
      inlineOffsetX: inlineOffsetX,
      inlineOffsetY: inlineOffsetY,
      inlineContainer: inlineContainer,
      sourceAttribute: sourceAttribute,
      zoomFactor: zoomFactor,
      paneContainer: paneContainer,
      inlinePane: inlinePane,
      handleTouch: handleTouch,
      onShow: onShow,
      onHide: onHide,
      injectBaseStyles: injectBaseStyles,
      hoverDelay: hoverDelay,
      touchDelay: touchDelay,
      hoverBoundingBox: hoverBoundingBox,
      touchBoundingBox: touchBoundingBox,
      boundingBoxContainer: boundingBoxContainer
    };

    if (this.settings.injectBaseStyles) {
      injectBaseStylesheet();
    }

    this._buildZoomPane();

    this._buildTrigger();
  }

  _createClass(Drift, [{
    key: "_buildZoomPane",
    value: function _buildZoomPane() {
      this.zoomPane = new ZoomPane({
        container: this.settings.paneContainer,
        zoomFactor: this.settings.zoomFactor,
        showWhitespaceAtEdges: this.settings.showWhitespaceAtEdges,
        containInline: this.settings.containInline,
        inline: this.settings.inlinePane,
        namespace: this.settings.namespace,
        inlineOffsetX: this.settings.inlineOffsetX,
        inlineOffsetY: this.settings.inlineOffsetY,
        inlineContainer: this.settings.inlineContainer
      });
    }
  }, {
    key: "_buildTrigger",
    value: function _buildTrigger() {
      this.trigger = new Trigger({
        el: this.triggerEl,
        zoomPane: this.zoomPane,
        handleTouch: this.settings.handleTouch,
        onShow: this.settings.onShow,
        onHide: this.settings.onHide,
        sourceAttribute: this.settings.sourceAttribute,
        hoverDelay: this.settings.hoverDelay,
        touchDelay: this.settings.touchDelay,
        hoverBoundingBox: this.settings.hoverBoundingBox,
        touchBoundingBox: this.settings.touchBoundingBox,
        namespace: this.settings.namespace,
        zoomFactor: this.settings.zoomFactor,
        boundingBoxContainer: this.settings.boundingBoxContainer
      });
    }
  }, {
    key: "setZoomImageURL",
    value: function setZoomImageURL(imageURL) {
      this.zoomPane._setImageURL(imageURL);
    }
  }, {
    key: "disable",
    value: function disable() {
      this.trigger.enabled = false;
    }
  }, {
    key: "enable",
    value: function enable() {
      this.trigger.enabled = true;
    }
  }, {
    key: "destroy",
    value: function destroy() {
      this.trigger._hide();

      this.trigger._unbindEvents();
    }
  }, {
    key: "isShowing",
    get: function get() {
      return this.zoomPane.isShowing;
    }
  }, {
    key: "zoomFactor",
    get: function get() {
      return this.settings.zoomFactor;
    },
    set: function set(zf) {
      this.settings.zoomFactor = zf;
      this.zoomPane.settings.zoomFactor = zf;
      this.trigger.settings.zoomFactor = zf;
      this.boundingBox.settings.zoomFactor = zf;
    }
  }]);

  return Drift;
}(); // Public API

/* eslint-disable no-self-assign */


export { Drift as default };
Object.defineProperty(Drift.prototype, "isShowing", {
  get: function get() {
    return this.isShowing;
  }
});
Object.defineProperty(Drift.prototype, "zoomFactor", {
  get: function get() {
    return this.zoomFactor;
  },
  set: function set(value) {
    this.zoomFactor = value;
  }
});
Drift.prototype["setZoomImageURL"] = Drift.prototype.setZoomImageURL;
Drift.prototype["disable"] = Drift.prototype.disable;
Drift.prototype["enable"] = Drift.prototype.enable;
Drift.prototype["destroy"] = Drift.prototype.destroy;
/* eslint-enable no-self-assign */
//# sourceMappingURL=Drift.js.map