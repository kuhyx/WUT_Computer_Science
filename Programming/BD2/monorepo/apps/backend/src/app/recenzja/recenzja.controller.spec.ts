import { Test, TestingModule } from '@nestjs/testing';
import { RecenzjaController } from './recenzja.controller';

describe('RecenzjaController', () => {
  let controller: RecenzjaController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [RecenzjaController],
    }).compile();

    controller = module.get<RecenzjaController>(RecenzjaController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
