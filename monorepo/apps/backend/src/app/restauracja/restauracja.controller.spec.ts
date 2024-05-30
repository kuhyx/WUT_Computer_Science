import { Test, TestingModule } from '@nestjs/testing';
import { RestauracjaController } from './restauracja.controller';

describe('RestauracjaController', () => {
  let controller: RestauracjaController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [RestauracjaController],
    }).compile();

    controller = module.get<RestauracjaController>(RestauracjaController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
