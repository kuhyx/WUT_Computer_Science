// src/znizka/znizka.controller.ts
import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { ZnizkaService } from './znizka.service';
import { Znizka } from '@prisma/client';

@Controller('znizka')
export class ZnizkaController {
  constructor(private readonly znizkaService: ZnizkaService) {}

  @Get()
  async findAll(): Promise<Znizka[]> {
    return this.znizkaService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Znizka | null> {
    return this.znizkaService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { kod: string; wartosc: number; czy_dostepna: boolean; restauracjaId: number }): Promise<Znizka> {
    return this.znizkaService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Znizka>): Promise<Znizka> {
    return this.znizkaService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Znizka> {
    return this.znizkaService.delete(+id);
  }
}
