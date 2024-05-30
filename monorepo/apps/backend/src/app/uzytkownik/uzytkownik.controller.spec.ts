import { Test, TestingModule } from '@nestjs/testing';
import { UzytkownikController } from './uzytkownik.controller';

describe('UzytkownikController', () => {
  let controller: UzytkownikController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UzytkownikController],
    }).compile();

    controller = module.get<UzytkownikController>(UzytkownikController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
