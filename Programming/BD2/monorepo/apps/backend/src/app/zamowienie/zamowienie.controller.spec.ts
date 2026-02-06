import { Test, TestingModule } from '@nestjs/testing';
import { ZamowienieController } from './zamowienie.controller';

describe('ZamowienieController', () => {
  let controller: ZamowienieController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ZamowienieController],
    }).compile();

    controller = module.get<ZamowienieController>(ZamowienieController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
