/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.richTextFormField', function () {
  'use strict';
  let viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components
      .getViewModel('richTextFormField');
    spyOn(viewModel, 'dispatch');
    viewModel.attr('fieldId', 'id');
  });

  it('does not fire valueChanged event on first value assignation', function () {
    viewModel.attr('value', '');
    expect(viewModel.dispatch).not.toHaveBeenCalled();
  });

  it('sets the value of the input', function () {
    viewModel.attr('value', 'test');
    expect(viewModel.attr('inputValue')).toEqual('test');
  });

  it('fires valueChanged event on input value change', function () {
    viewModel.attr('value', '');
    viewModel.attr('inputValue', 'newValue');
    viewModel.onBlur();
    expect(viewModel.dispatch).toHaveBeenCalledWith({
      type: 'valueChanged',
      fieldId: 'id',
      value: 'newValue',
    });
    viewModel.attr('inputValue', 'newValue2');
    viewModel.onBlur();
    expect(viewModel.dispatch).toHaveBeenCalledWith({
      type: 'valueChanged',
      fieldId: 'id',
      value: 'newValue2',
    });
  });

  describe('isAllowToSet() method', () => {
    it('should return TRUE. has focus and values are equal', () => {
      let value = 'myText';
      viewModel.attr('_value', value);
      viewModel.attr('_oldValue', value);
      viewModel.attr('editorHasFocus', true);

      let isAllow = viewModel.isAllowToSet();

      expect(isAllow).toBeTruthy();
    });

    it('should return TRUE. doesn\'t have focus and values are equal', () => {
      let value = 'myText';
      viewModel.attr('_value', value);
      viewModel.attr('_oldValue', value);
      viewModel.attr('editorHasFocus', false);

      let isAllow = viewModel.isAllowToSet();

      expect(isAllow).toBeTruthy();
    });

    it('should return TRUE. doesn\'t have focus and values NOT are equal',
      () => {
        let value = 'myText';
        viewModel.attr('_value', value);
        viewModel.attr('_oldValue', 'myTex');
        viewModel.attr('editorHasFocus', false);

        let isAllow = viewModel.isAllowToSet();

        expect(isAllow).toBeTruthy();
      }
    );

    it('should return FALSE. has focus and values are NOT equal', () => {
      let value = 'myText';
      viewModel.attr('_value', value);
      viewModel.attr('_oldValue', 'myTex');
      viewModel.attr('editorHasFocus', true);

      let isAllow = viewModel.isAllowToSet();

      expect(isAllow).toBeFalsy();
    });
  });
});
