"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _throwIfMissing = _interopRequireDefault(require("./util/throwIfMissing"));

var _dom = require("./util/dom");

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

// All officially-supported browsers have this, but it's easy to
// account for, just in case.
var divStyle = document.createElement("div").style;
var HAS_ANIMATION = typeof document === "undefined" ? false : "animation" in divStyle || "webkitAnimation" in divStyle;

var ZoomPane =
/*#__PURE__*/
function () {
  function ZoomPane() {
    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

    _classCallCheck(this, ZoomPane);

    this._completeShow = this._completeShow.bind(this);
    this._completeHide = this._completeHide.bind(this);
    this._handleLoad = this._handleLoad.bind(this);
    this.isShowing = false;
    var _options$container = options.container,
        container = _options$container === void 0 ? null : _options$container,
        _options$zoomFactor = options.zoomFactor,
        zoomFactor = _options$zoomFactor === void 0 ? (0, _throwIfMissing.default)() : _options$zoomFactor,
        _options$inline = options.inline,
        inline = _options$inline === void 0 ? (0, _throwIfMissing.default)() : _options$inline,
        _options$namespace = options.namespace,
        namespace = _options$namespace === void 0 ? null : _options$namespace,
        _options$showWhitespa = options.showWhitespaceAtEdges,
        showWhitespaceAtEdges = _options$showWhitespa === void 0 ? (0, _throwIfMissing.default)() : _options$showWhitespa,
        _options$containInlin = options.containInline,
        containInline = _options$containInlin === void 0 ? (0, _throwIfMissing.default)() : _options$containInlin,
        _options$inlineOffset = options.inlineOffsetX,
        inlineOffsetX = _options$inlineOffset === void 0 ? 0 : _options$inlineOffset,
        _options$inlineOffset2 = options.inlineOffsetY,
        inlineOffsetY = _options$inlineOffset2 === void 0 ? 0 : _options$inlineOffset2,
        _options$inlineContai = options.inlineContainer,
        inlineContainer = _options$inlineContai === void 0 ? document.body : _options$inlineContai;
    this.settings = {
      container: container,
      zoomFactor: zoomFactor,
      inline: inline,
      namespace: namespace,
      showWhitespaceAtEdges: showWhitespaceAtEdges,
      containInline: containInline,
      inlineOffsetX: inlineOffsetX,
      inlineOffsetY: inlineOffsetY,
      inlineContainer: inlineContainer
    };
    this.openClasses = this._buildClasses("open");
    this.openingClasses = this._buildClasses("opening");
    this.closingClasses = this._buildClasses("closing");
    this.inlineClasses = this._buildClasses("inline");
    this.loadingClasses = this._buildClasses("loading");

    this._buildElement();
  }

  _createClass(ZoomPane, [{
    key: "_buildClasses",
    value: function _buildClasses(suffix) {
      var classes = ["drift-".concat(suffix)];
      var ns = this.settings.namespace;

      if (ns) {
        classes.push("".concat(ns, "-").concat(suffix));
      }

      return classes;
    }
  }, {
    key: "_buildElement",
    value: function _buildElement() {
      this.el = document.createElement("div");
      (0, _dom.addClasses)(this.el, this._buildClasses("zoom-pane"));
      var loaderEl = document.createElement("div");
      (0, _dom.addClasses)(loaderEl, this._buildClasses("zoom-pane-loader"));
      this.el.appendChild(loaderEl);
      this.imgEl = document.createElement("img");
      this.el.appendChild(this.imgEl);
    }
  }, {
    key: "_setImageURL",
    value: function _setImageURL(imageURL) {
      this.imgEl.setAttribute("src", imageURL);
    }
  }, {
    key: "_setImageSize",
    value: function _setImageSize(triggerWidth, triggerHeight) {
      this.imgEl.style.width = "".concat(triggerWidth * this.settings.zoomFactor, "px");
      this.imgEl.style.height = "".concat(triggerHeight * this.settings.zoomFactor, "px");
    } // `percentageOffsetX` and `percentageOffsetY` must be percentages
    // expressed as floats between `0' and `1`.

  }, {
    key: "setPosition",
    value: function setPosition(percentageOffsetX, percentageOffsetY, triggerRect) {
      var imgElWidth = this.imgEl.offsetWidth;
      var imgElHeight = this.imgEl.offsetHeight;
      var elWidth = this.el.offsetWidth;
      var elHeight = this.el.offsetHeight;
      var centreOfContainerX = elWidth / 2;
      var centreOfContainerY = elHeight / 2;
      var targetImgXToBeCentre = imgElWidth * percentageOffsetX;
      var targetImgYToBeCentre = imgElHeight * percentageOffsetY;
      var left = centreOfContainerX - targetImgXToBeCentre;
      var top = centreOfContainerY - targetImgYToBeCentre;
      var differenceBetweenContainerWidthAndImgWidth = elWidth - imgElWidth;
      var differenceBetweenContainerHeightAndImgHeight = elHeight - imgElHeight;
      var isContainerLargerThanImgX = differenceBetweenContainerWidthAndImgWidth > 0;
      var isContainerLargerThanImgY = differenceBetweenContainerHeightAndImgHeight > 0;
      var minLeft = isContainerLargerThanImgX ? differenceBetweenContainerWidthAndImgWidth / 2 : 0;
      var minTop = isContainerLargerThanImgY ? differenceBetweenContainerHeightAndImgHeight / 2 : 0;
      var maxLeft = isContainerLargerThanImgX ? differenceBetweenContainerWidthAndImgWidth / 2 : differenceBetweenContainerWidthAndImgWidth;
      var maxTop = isContainerLargerThanImgY ? differenceBetweenContainerHeightAndImgHeight / 2 : differenceBetweenContainerHeightAndImgHeight;

      if (this.el.parentElement === this.settings.inlineContainer) {
        // This may be needed in the future to deal with browser event
        // inconsistencies, but it's difficult to tell for sure.
        // let scrollX = isTouch ? 0 : window.scrollX;
        // let scrollY = isTouch ? 0 : window.scrollY;
        var scrollX = window.pageXOffset;
        var scrollY = window.pageYOffset;
        var inlineLeft = triggerRect.left + percentageOffsetX * triggerRect.width - elWidth / 2 + this.settings.inlineOffsetX + scrollX;
        var inlineTop = triggerRect.top + percentageOffsetY * triggerRect.height - elHeight / 2 + this.settings.inlineOffsetY + scrollY;

        if (this.settings.containInline) {
          if (inlineLeft < triggerRect.left + scrollX) {
            inlineLeft = triggerRect.left + scrollX;
          } else if (inlineLeft + elWidth > triggerRect.left + triggerRect.width + scrollX) {
            inlineLeft = triggerRect.left + triggerRect.width - elWidth + scrollX;
          }

          if (inlineTop < triggerRect.top + scrollY) {
            inlineTop = triggerRect.top + scrollY;
          } else if (inlineTop + elHeight > triggerRect.top + triggerRect.height + scrollY) {
            inlineTop = triggerRect.top + triggerRect.height - elHeight + scrollY;
          }
        }

        this.el.style.left = "".concat(inlineLeft, "px");
        this.el.style.top = "".concat(inlineTop, "px");
      }

      if (!this.settings.showWhitespaceAtEdges) {
        if (left > minLeft) {
          left = minLeft;
        } else if (left < maxLeft) {
          left = maxLeft;
        }

        if (top > minTop) {
          top = minTop;
        } else if (top < maxTop) {
          top = maxTop;
        }
      }

      this.imgEl.style.transform = "translate(".concat(left, "px, ").concat(top, "px)");
      this.imgEl.style.webkitTransform = "translate(".concat(left, "px, ").concat(top, "px)");
    }
  }, {
    key: "_removeListenersAndResetClasses",
    value: function _removeListenersAndResetClasses() {
      this.el.removeEventListener("animationend", this._completeShow, false);
      this.el.removeEventListener("animationend", this._completeHide, false);
      this.el.removeEventListener("webkitAnimationEnd", this._completeShow, false);
      this.el.removeEventListener("webkitAnimationEnd", this._completeHide, false);
      (0, _dom.removeClasses)(this.el, this.openClasses);
      (0, _dom.removeClasses)(this.el, this.closingClasses);
    }
  }, {
    key: "show",
    value: function show(imageURL, triggerWidth, triggerHeight) {
      this._removeListenersAndResetClasses();

      this.isShowing = true;
      (0, _dom.addClasses)(this.el, this.openClasses);

      if (this.imgEl.getAttribute("src") != imageURL) {
        (0, _dom.addClasses)(this.el, this.loadingClasses);
        this.imgEl.addEventListener("load", this._handleLoad, false);

        this._setImageURL(imageURL);
      }

      this._setImageSize(triggerWidth, triggerHeight);

      if (this._isInline) {
        this._showInline();
      } else {
        this._showInContainer();
      }

      if (HAS_ANIMATION) {
        this.el.addEventListener("animationend", this._completeShow, false);
        this.el.addEventListener("webkitAnimationEnd", this._completeShow, false);
        (0, _dom.addClasses)(this.el, this.openingClasses);
      }
    }
  }, {
    key: "_showInline",
    value: function _showInline() {
      this.settings.inlineContainer.appendChild(this.el);
      (0, _dom.addClasses)(this.el, this.inlineClasses);
    }
  }, {
    key: "_showInContainer",
    value: function _showInContainer() {
      this.settings.container.appendChild(this.el);
    }
  }, {
    key: "hide",
    value: function hide() {
      this._removeListenersAndResetClasses();

      this.isShowing = false;

      if (HAS_ANIMATION) {
        this.el.addEventListener("animationend", this._completeHide, false);
        this.el.addEventListener("webkitAnimationEnd", this._completeHide, false);
        (0, _dom.addClasses)(this.el, this.closingClasses);
      } else {
        (0, _dom.removeClasses)(this.el, this.openClasses);
        (0, _dom.removeClasses)(this.el, this.inlineClasses);
      }
    }
  }, {
    key: "_completeShow",
    value: function _completeShow() {
      this.el.removeEventListener("animationend", this._completeShow, false);
      this.el.removeEventListener("webkitAnimationEnd", this._completeShow, false);
      (0, _dom.removeClasses)(this.el, this.openingClasses);
    }
  }, {
    key: "_completeHide",
    value: function _completeHide() {
      this.el.removeEventListener("animationend", this._completeHide, false);
      this.el.removeEventListener("webkitAnimationEnd", this._completeHide, false);
      (0, _dom.removeClasses)(this.el, this.openClasses);
      (0, _dom.removeClasses)(this.el, this.closingClasses);
      (0, _dom.removeClasses)(this.el, this.inlineClasses);
      this.el.setAttribute("style", ""); // The window could have been resized above or below `inline`
      // limits since the ZoomPane was shown. Because of this, we
      // can't rely on `this._isInline` here.

      if (this.el.parentElement === this.settings.container) {
        this.settings.container.removeChild(this.el);
      } else if (this.el.parentElement === this.settings.inlineContainer) {
        this.settings.inlineContainer.removeChild(this.el);
      }
    }
  }, {
    key: "_handleLoad",
    value: function _handleLoad() {
      this.imgEl.removeEventListener("load", this._handleLoad, false);
      (0, _dom.removeClasses)(this.el, this.loadingClasses);
    }
  }, {
    key: "_isInline",
    get: function get() {
      var inline = this.settings.inline;
      return inline === true || typeof inline === "number" && window.innerWidth <= inline;
    }
  }]);

  return ZoomPane;
}();

exports.default = ZoomPane;
//# sourceMappingURL=ZoomPane.js.map