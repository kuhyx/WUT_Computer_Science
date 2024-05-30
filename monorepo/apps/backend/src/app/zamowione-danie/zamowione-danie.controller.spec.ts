import { Test, TestingModule } from '@nestjs/testing';
import { ZamowioneDanieController } from './zamowione-danie.controller';

describe('ZamowioneDanieController', () => {
  let controller: ZamowioneDanieController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ZamowioneDanieController],
    }).compile();

    controller = module.get<ZamowioneDanieController>(ZamowioneDanieController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
