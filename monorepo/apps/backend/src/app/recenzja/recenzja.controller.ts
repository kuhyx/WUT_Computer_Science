// src/recenzja/recenzja.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { RecenzjaService } from './recenzja.service';
import { Recenzja } from '@prisma/client';

@Controller('recenzja')
export class RecenzjaController {
  constructor(private readonly recenzjaService: RecenzjaService) {}

  @Get()
  async findAll(): Promise<Recenzja[]> {
    return this.recenzjaService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Recenzja | null> {
    return this.recenzjaService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { tekst: string; wartosc: number; restauracjaId: number; uzytkownikId: number }): Promise<Recenzja> {
    return this.recenzjaService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Recenzja>): Promise<Recenzja> {
    return this.recenzjaService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Recenzja> {
    return this.recenzjaService.delete(+id);
  }
}
