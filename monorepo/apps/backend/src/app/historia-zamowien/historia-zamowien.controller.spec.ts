import { Test, TestingModule } from '@nestjs/testing';
import { HistoriaZamowienController } from './historia-zamowien.controller';

describe('HistoriaZamowienController', () => {
  let controller: HistoriaZamowienController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [HistoriaZamowienController],
    }).compile();

    controller = module.get<HistoriaZamowienController>(
      HistoriaZamowienController
    );
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
