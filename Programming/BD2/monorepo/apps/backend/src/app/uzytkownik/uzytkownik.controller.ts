// src/uzytkownik/uzytkownik.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { UzytkownikService } from './uzytkownik.service';
import { Uzytkownik } from '@prisma/client';

@Controller('uzytkownik')
export class UzytkownikController {
  constructor(private readonly uzytkownikService: UzytkownikService) {}

  @Get()
  async findAll(): Promise<Uzytkownik[]> {
    return this.uzytkownikService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Uzytkownik | null> {
    return this.uzytkownikService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { imie: string; nazwisko: string; adres: string; Historia_zamowienId: number }): Promise<Uzytkownik> {
    return this.uzytkownikService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Uzytkownik>): Promise<Uzytkownik> {
    return this.uzytkownikService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Uzytkownik> {
    return this.uzytkownikService.delete(+id);
  }
}
