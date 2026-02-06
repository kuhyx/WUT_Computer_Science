import { Test, TestingModule } from '@nestjs/testing';
import { ZnizkaController } from './znizka.controller';

describe('ZnizkaController', () => {
  let controller: ZnizkaController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ZnizkaController],
    }).compile();

    controller = module.get<ZnizkaController>(ZnizkaController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
