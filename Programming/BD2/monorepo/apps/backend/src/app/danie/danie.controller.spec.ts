import { Test, TestingModule } from '@nestjs/testing';
import { DanieController } from './danie.controller';

describe('DanieController', () => {
  let controller: DanieController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [DanieController],
    }).compile();

    controller = module.get<DanieController>(DanieController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
