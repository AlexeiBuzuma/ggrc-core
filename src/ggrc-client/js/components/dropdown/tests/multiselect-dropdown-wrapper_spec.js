/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../multiselect-dropdown-wrapper';

describe('multiselectDropdownWrapper component', function () {
  let viewModel;
  let response;
  let findDfd;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
    response = [
      {
        id: 1,
        name: '1 item',
        extra: 'extra',
      },
      {
        id: 2,
        name: '2 item',
        extra: 'extra',
      },
      {
        id: 3,
        name: '3 item',
        extra: 'extra',
      },
      {
        id: 4,
        name: '4 item',
        extra: 'extra',
      },
    ];

    findDfd = can.Deferred();
    CMS.Models.TestType = can.Map.extend({
      findAll: jasmine.createSpy('findAll').and.returnValue(findDfd),
      findInCacheById: jasmine.createSpy('findInCacheById')
        .and.returnValue({
          id: 'testId',
          name: 'testName',
          extra: 'extra',
        }),
    }, {});
  });

  describe('modelName set()', () => {
    it('calls findAll()', () => {
      viewModel.attr('modelName', 'TestType');

      expect(CMS.Models.TestType.findAll).toHaveBeenCalled();
    });

    it('calls prepareOptions()', (done) => {
      spyOn(viewModel, 'prepareOptions');

      viewModel.attr('modelName', 'TestType');
      findDfd.resolve(response);

      findDfd.then((result) => {
        expect(viewModel.prepareOptions).toHaveBeenCalledWith(response);

        done();
      });
    });

    describe('prepareOptions() method', () => {
      beforeEach(function () {
        viewModel.attr('selected', [
          {
            id: 2,
            name: '2 item',
            extra: 'extra',
          },
          {
            id: 3,
            name: '3 item',
            extra: 'extra',
          },
        ]);
      });

      it('sets preparedOptions', (done) => {
        viewModel.attr('modelName', 'TestType');
        findDfd.resolve(response);

        findDfd.then((result) => {
          expect(viewModel.preparedOptions.length).toEqual(response.length);

          done();
        });
      });

      it('converts models to a correct format', (done) => {
        viewModel.attr('modelName', 'TestType');
        findDfd.resolve(response);

        findDfd.then((result) => {
          expect(viewModel.preparedOptions[0].value).toEqual('1 item');
          expect(viewModel.preparedOptions[0].id).toEqual(1);
          expect(viewModel.preparedOptions[0].checked).toBeFalsy();
          expect(viewModel.preparedOptions[0].extra).toBeUndefined();

          done();
        });
      });

      it('sets selectedInternal', (done) => {
        viewModel.attr('modelName', 'TestType');
        findDfd.resolve(response);

        findDfd.then((result) => {
          expect(viewModel.selectedInternal.length)
            .toEqual(viewModel.selected.length);

          done();
        });
      });

      it('selectedInternal has correct format', (done) => {
        viewModel.attr('modelName', 'TestType');
        findDfd.resolve(response);

        findDfd.then((result) => {
          expect(viewModel.selectedInternal[0].value).toEqual('2 item');
          expect(viewModel.selectedInternal[0].id).toEqual(2);
          expect(viewModel.selectedInternal[0].checked).toBeTruthy();
          expect(viewModel.selectedInternal[0].extra).toBeUndefined();

          done();
        });
      });
    });
  });

  describe('events', () => {
    let events;
    let handler;
    let newSelected;

    beforeEach(function () {
      viewModel.attr('modelName', 'TestType');
      viewModel.attr('selected', [
        {
          id: 2,
          name: '2 item',
          extra: 'extra',
        },
        {
          id: 3,
          name: '3 item',
          extra: 'extra',
        },
      ]);

      events = Component.prototype.events;
      handler = events['multiselect-dropdown multiselect:changed']
        .bind({viewModel: viewModel});

      newSelected = [{id: 1}];
    });

    it('should call findInCacheById', () => {
      handler({}, {}, newSelected);

      expect(CMS.Models.TestType.findInCacheById).toHaveBeenCalled();
    });

    it('should get model from cache', () => {
      handler({}, {}, newSelected);

      expect(viewModel.selected.length).toEqual(newSelected.length);
      expect(viewModel.selected[0].id).toEqual('testId');
      expect(viewModel.selected[0].name).toEqual('testName');
      expect(viewModel.selected[0].extra).toEqual('extra');
    });

    it('should keep an object', () => {
      let initialObj = viewModel.selected;
      handler({}, {}, newSelected);
      expect(viewModel.selected).toEqual(initialObj);
    });
  });
});
