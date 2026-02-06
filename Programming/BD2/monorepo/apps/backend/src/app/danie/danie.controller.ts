import { Controller, Get, Post, Put, Delete, Param, Body } from '@nestjs/common';
import { DanieService } from './danie.service';
import { Danie } from '@prisma/client';

@Controller('danie')
export class DanieController {
  constructor(private readonly danieService: DanieService) {}

  @Get()
  async findAll(): Promise<Danie[]> {
    return this.danieService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string): Promise<Danie | null> {
    return this.danieService.findOne(+id);
  }

  @Post()
  async create(@Body() data: { cena: number; kategoria: string; nazwa: string }): Promise<Danie> {
    return this.danieService.create(data);
  }

  @Put(':id')
  async update(@Param('id') id: string, @Body() data: Partial<Danie>): Promise<Danie> {
    return this.danieService.update(+id, data);
  }

  @Delete(':id')
  async delete(@Param('id') id: string): Promise<Danie> {
    return this.danieService.delete(+id);
  }
}
