function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

import throwIfMissing from "./util/throwIfMissing";
import BoundingBox from "./BoundingBox";

var Trigger =
/*#__PURE__*/
function () {
  function Trigger() {
    var options = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : {};

    _classCallCheck(this, Trigger);

    this._show = this._show.bind(this);
    this._hide = this._hide.bind(this);
    this._handleEntry = this._handleEntry.bind(this);
    this._handleMovement = this._handleMovement.bind(this);
    var _options$el = options.el,
        el = _options$el === void 0 ? throwIfMissing() : _options$el,
        _options$zoomPane = options.zoomPane,
        zoomPane = _options$zoomPane === void 0 ? throwIfMissing() : _options$zoomPane,
        _options$sourceAttrib = options.sourceAttribute,
        sourceAttribute = _options$sourceAttrib === void 0 ? throwIfMissing() : _options$sourceAttrib,
        _options$handleTouch = options.handleTouch,
        handleTouch = _options$handleTouch === void 0 ? throwIfMissing() : _options$handleTouch,
        _options$onShow = options.onShow,
        onShow = _options$onShow === void 0 ? null : _options$onShow,
        _options$onHide = options.onHide,
        onHide = _options$onHide === void 0 ? null : _options$onHide,
        _options$hoverDelay = options.hoverDelay,
        hoverDelay = _options$hoverDelay === void 0 ? 0 : _options$hoverDelay,
        _options$touchDelay = options.touchDelay,
        touchDelay = _options$touchDelay === void 0 ? 0 : _options$touchDelay,
        _options$hoverBoundin = options.hoverBoundingBox,
        hoverBoundingBox = _options$hoverBoundin === void 0 ? throwIfMissing() : _options$hoverBoundin,
        _options$touchBoundin = options.touchBoundingBox,
        touchBoundingBox = _options$touchBoundin === void 0 ? throwIfMissing() : _options$touchBoundin,
        _options$namespace = options.namespace,
        namespace = _options$namespace === void 0 ? null : _options$namespace,
        _options$zoomFactor = options.zoomFactor,
        zoomFactor = _options$zoomFactor === void 0 ? throwIfMissing() : _options$zoomFactor,
        _options$boundingBoxC = options.boundingBoxContainer,
        boundingBoxContainer = _options$boundingBoxC === void 0 ? throwIfMissing() : _options$boundingBoxC;
    this.settings = {
      el: el,
      zoomPane: zoomPane,
      sourceAttribute: sourceAttribute,
      handleTouch: handleTouch,
      onShow: onShow,
      onHide: onHide,
      hoverDelay: hoverDelay,
      touchDelay: touchDelay,
      hoverBoundingBox: hoverBoundingBox,
      touchBoundingBox: touchBoundingBox,
      namespace: namespace,
      zoomFactor: zoomFactor,
      boundingBoxContainer: boundingBoxContainer
    };

    if (this.settings.hoverBoundingBox || this.settings.touchBoundingBox) {
      this.boundingBox = new BoundingBox({
        namespace: this.settings.namespace,
        zoomFactor: this.settings.zoomFactor,
        containerEl: this.settings.boundingBoxContainer
      });
    }

    this.enabled = true;

    this._bindEvents();
  }

  _createClass(Trigger, [{
    key: "_preventDefault",
    value: function _preventDefault(event) {
      event.preventDefault();
    }
  }, {
    key: "_preventDefaultAllowTouchScroll",
    value: function _preventDefaultAllowTouchScroll(event) {
      if (!this.settings.touchDelay || !this._isTouchEvent(event) || this.isShowing) {
        event.preventDefault();
      }
    }
  }, {
    key: "_isTouchEvent",
    value: function _isTouchEvent(event) {
      return !!event.touches;
    }
  }, {
    key: "_bindEvents",
    value: function _bindEvents() {
      this.settings.el.addEventListener("mouseenter", this._handleEntry, false);
      this.settings.el.addEventListener("mouseleave", this._hide, false);
      this.settings.el.addEventListener("mousemove", this._handleMovement, false);

      if (this.settings.handleTouch) {
        this.settings.el.addEventListener("touchstart", this._handleEntry, false);
        this.settings.el.addEventListener("touchend", this._hide, false);
        this.settings.el.addEventListener("touchmove", this._handleMovement, false);
      } else {
        this.settings.el.addEventListener("touchstart", this._preventDefault, false);
        this.settings.el.addEventListener("touchend", this._preventDefault, false);
        this.settings.el.addEventListener("touchmove", this._preventDefault, false);
      }
    }
  }, {
    key: "_unbindEvents",
    value: function _unbindEvents() {
      this.settings.el.removeEventListener("mouseenter", this._handleEntry, false);
      this.settings.el.removeEventListener("mouseleave", this._hide, false);
      this.settings.el.removeEventListener("mousemove", this._handleMovement, false);

      if (this.settings.handleTouch) {
        this.settings.el.removeEventListener("touchstart", this._handleEntry, false);
        this.settings.el.removeEventListener("touchend", this._hide, false);
        this.settings.el.removeEventListener("touchmove", this._handleMovement, false);
      } else {
        this.settings.el.removeEventListener("touchstart", this._preventDefault, false);
        this.settings.el.removeEventListener("touchend", this._preventDefault, false);
        this.settings.el.removeEventListener("touchmove", this._preventDefault, false);
      }
    }
  }, {
    key: "_handleEntry",
    value: function _handleEntry(e) {
      this._preventDefaultAllowTouchScroll(e);

      this._lastMovement = e;

      if (e.type == "mouseenter" && this.settings.hoverDelay) {
        this.entryTimeout = setTimeout(this._show, this.settings.hoverDelay);
      } else if (this.settings.touchDelay) {
        this.entryTimeout = setTimeout(this._show, this.settings.touchDelay);
      } else {
        this._show();
      }
    }
  }, {
    key: "_show",
    value: function _show() {
      if (!this.enabled) {
        return;
      }

      var onShow = this.settings.onShow;

      if (onShow && typeof onShow === "function") {
        onShow();
      }

      this.settings.zoomPane.show(this.settings.el.getAttribute(this.settings.sourceAttribute), this.settings.el.clientWidth, this.settings.el.clientHeight);

      if (this._lastMovement) {
        var touchActivated = this._lastMovement.touches;

        if (touchActivated && this.settings.touchBoundingBox || !touchActivated && this.settings.hoverBoundingBox) {
          this.boundingBox.show(this.settings.zoomPane.el.clientWidth, this.settings.zoomPane.el.clientHeight);
        }
      }

      this._handleMovement();
    }
  }, {
    key: "_hide",
    value: function _hide(e) {
      if (e) {
        this._preventDefaultAllowTouchScroll(e);
      }

      this._lastMovement = null;

      if (this.entryTimeout) {
        clearTimeout(this.entryTimeout);
      }

      if (this.boundingBox) {
        this.boundingBox.hide();
      }

      var onHide = this.settings.onHide;

      if (onHide && typeof onHide === "function") {
        onHide();
      }

      this.settings.zoomPane.hide();
    }
  }, {
    key: "_handleMovement",
    value: function _handleMovement(e) {
      if (e) {
        this._preventDefaultAllowTouchScroll(e);

        this._lastMovement = e;
      } else if (this._lastMovement) {
        e = this._lastMovement;
      } else {
        return;
      }

      var movementX;
      var movementY;

      if (e.touches) {
        var firstTouch = e.touches[0];
        movementX = firstTouch.clientX;
        movementY = firstTouch.clientY;
      } else {
        movementX = e.clientX;
        movementY = e.clientY;
      }

      var el = this.settings.el;
      var rect = el.getBoundingClientRect();
      var offsetX = movementX - rect.left;
      var offsetY = movementY - rect.top;
      var percentageOffsetX = offsetX / this.settings.el.clientWidth;
      var percentageOffsetY = offsetY / this.settings.el.clientHeight;

      if (this.boundingBox) {
        this.boundingBox.setPosition(percentageOffsetX, percentageOffsetY, rect);
      }

      this.settings.zoomPane.setPosition(percentageOffsetX, percentageOffsetY, rect);
    }
  }, {
    key: "isShowing",
    get: function get() {
      return this.settings.zoomPane.isShowing;
    }
  }]);

  return Trigger;
}();

export { Trigger as default };
//# sourceMappingURL=Trigger.js.map