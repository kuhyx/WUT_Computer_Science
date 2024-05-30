// src/historia-zamowien/historia-zamowien.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { HistoriaZamowienService } from './historia-zamowien.service';
import { Historia_zamowien } from '@prisma/client';

@Controller('historia-zamowien')
export class HistoriaZamowienController {
  constructor(private readonly historiaZamowienService: HistoriaZamowienService) {}

  @Get()
  async findAll(): Promise<Historia_zamowien[]> {
    return this.historiaZamowienService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Historia_zamowien | null> {
    return this.historiaZamowienService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { data_zamowienia: Date }): Promise<Historia_zamowien> {
    return this.historiaZamowienService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Historia_zamowien>): Promise<Historia_zamowien> {
    return this.historiaZamowienService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Historia_zamowien> {
    return this.historiaZamowienService.delete(+id);
  }
}
